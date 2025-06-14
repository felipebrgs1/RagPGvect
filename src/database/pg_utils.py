import psycopg2
from psycopg2 import sql
from ..config.settings import get_pg_credentials, get_pg_connection_string

def _get_raw_connection(db_name: str = None):
    """
    Retorna uma conexão bruta do psycopg2, útil para operações de setup.
    Por padrão, tenta conectar ao DB especificado em .env.
    Pode-se especificar 'postgres' para criar o DB principal.
    """
    creds = get_pg_credentials()
    if db_name:
        creds['database'] = db_name # Conecta a outro DB para criar o alvo
    
    return psycopg2.connect(
        host=creds['host'],
        port=creds['port'],
        user=creds['user'],
        password=creds['password'],
        database=creds['database']
    )

def setup_database_and_extension():
    """
    Cria o banco de dados e habilita a extensão pgvector.
    LangChain PGVector criará as tabelas se elas não existirem.
    """
    db_name = get_pg_credentials()['database']

    # 1. Conectar ao DB 'postgres' (ou outro padrão) para criar o DB alvo
    conn_default = None
    try:
        conn_default = _get_raw_connection(db_name="postgres")
        conn_default.autocommit = True
        cursor = conn_default.cursor()

        print(f"Verificando/criando banco de dados '{db_name}'...")
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"Banco de dados '{db_name}' já existe.")

    except Exception as e:
        print(f"Erro ao verificar/criar o banco de dados: {e}")
        # Se falhar aqui, não há como prosseguir
        raise
    finally:
        if conn_default:
            conn_default.close()

    # 2. Conectar ao DB alvo para habilitar a extensão pgvector
    conn_target = None
    try:
        conn_target = _get_raw_connection() # Agora conecta ao DB alvo
        conn_target.autocommit = True
        cursor = conn_target.cursor()

        print("Habilitando extensão 'vector' (pgvector)...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("Extensão 'vector' habilitada com sucesso.")
        
        # Opcional: Verificar/criar as tabelas que o LangChain PGVector usa.
        # LangChain PGVector cria essas tabelas automaticamente, mas tê-las aqui ajuda no debugging.
        print("Verificando/criando tabelas padrão do LangChain PGVector...")
        
        # Primeiro, verifica se a tabela existe e se tem todas as colunas necessárias
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'langchain_pg_embedding' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Cria a tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
                uuid uuid PRIMARY KEY,
                collection_id uuid,
                embedding vector(768), -- Dimensão do embedding do Gemini (embedding-001)
                document TEXT,
                cmetadata JSONB,
                custom_id TEXT
            );
        """)
        
        # Se a tabela já existia mas não tem a coluna custom_id, adiciona ela
        if existing_columns and 'custom_id' not in existing_columns:
            print("Adicionando coluna 'custom_id' à tabela 'langchain_pg_embedding'...")
            cursor.execute("ALTER TABLE langchain_pg_embedding ADD COLUMN custom_id TEXT;")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS langchain_pg_collection (
                uuid uuid PRIMARY KEY,
                name TEXT UNIQUE,
                cmetadata JSONB
            );
        """)
        print("Tabelas 'langchain_pg_embedding' e 'langchain_pg_collection' verificadas/criadas.")

    except Exception as e:
        print(f"Erro ao habilitar pgvector ou criar tabelas: {e}")
        raise
    finally:
        if conn_target:
            conn_target.close()