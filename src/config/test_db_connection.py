#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados PostgreSQL.
"""

import psycopg2
from sqlalchemy import create_engine, text

# Importa as configurações do mesmo diretório
from setting import load_environment_variables, get_pg_credentials, get_pg_connection_string

def test_psycopg2_connection():
    """Testa a conexão usando psycopg2 diretamente."""
    print("🔄 Testando conexão com psycopg2...")
    
    try:
        # Carrega as variáveis de ambiente
        load_environment_variables()
        
        # Obtém as credenciais
        credentials = get_pg_credentials()
        
        # Tenta conectar
        conn = psycopg2.connect(**credentials)
        cursor = conn.cursor()
        
        # Executa uma query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ Conexão psycopg2 bem-sucedida!")
        print(f"📊 Versão do PostgreSQL: {version[0]}")
        
        # Testa algumas informações básicas
        cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
        db_info = cursor.fetchone()
        
        print(f"🗄️  Database: {db_info[0]}")
        print(f"👤 Usuário: {db_info[1]}")
        print(f"🌐 Servidor: {db_info[2]}:{db_info[3]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão psycopg2: {e}")
        return False

def test_sqlalchemy_connection():
    """Testa a conexão usando SQLAlchemy (formato LangChain)."""
    print("\n🔄 Testando conexão com SQLAlchemy...")
    
    try:
        # Obtém a string de conexão
        connection_string = get_pg_connection_string()
        print(f"🔗 String de conexão: {connection_string.replace(connection_string.split('@')[0].split('//')[1], '***:***')}")
        
        # Cria o engine
        engine = create_engine(connection_string)
        
        # Testa a conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            
            print("✅ Conexão SQLAlchemy bem-sucedida!")
            print(f"📊 Versão do PostgreSQL: {version[0]}")
            
            # Testa informações básicas
            result = conn.execute(text("SELECT current_database(), current_user"))
            db_info = result.fetchone()
            
            print(f"🗄️  Database: {db_info[0]}")
            print(f"👤 Usuário: {db_info[1]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão SQLAlchemy: {e}")
        return False

def test_pgvector_extension():
    """Testa se a extensão pgvector está disponível."""
    print("\n🔄 Testando extensão pgvector...")
    
    try:
        credentials = get_pg_credentials()
        conn = psycopg2.connect(**credentials)
        cursor = conn.cursor()
        
        # Verifica se a extensão pgvector está instalada
        cursor.execute("""
            SELECT EXISTS(
                SELECT 1 FROM pg_extension WHERE extname = 'vector'
            );
        """)
        
        has_pgvector = cursor.fetchone()[0]
        
        if has_pgvector:
            print("✅ Extensão pgvector está instalada!")
            
            # Testa criação de um vetor simples
            cursor.execute("SELECT '[1,2,3]'::vector;")
            vector_result = cursor.fetchone()
            print(f"🧮 Teste de vetor: {vector_result[0]}")
            
        else:
            print("⚠️  Extensão pgvector NÃO está instalada.")
            print("💡 Para instalar, execute: CREATE EXTENSION vector;")
        
        cursor.close()
        conn.close()
        
        return has_pgvector
        
    except Exception as e:
        print(f"❌ Erro ao testar pgvector: {e}")
        return False

def main():
    """Função principal que executa todos os testes."""
    print("🚀 Iniciando testes de conexão com o banco de dados...\n")
    
    # Testa psycopg2
    psycopg2_ok = test_psycopg2_connection()
    
    # Testa SQLAlchemy
    sqlalchemy_ok = test_sqlalchemy_connection()
    
    # Testa pgvector
    pgvector_ok = test_pgvector_extension()
    
    # Resumo final
    print("\n" + "="*50)
    print("📋 RESUMO DOS TESTES:")
    print("="*50)
    print(f"psycopg2:     {'✅ OK' if psycopg2_ok else '❌ FALHOU'}")
    print(f"SQLAlchemy:   {'✅ OK' if sqlalchemy_ok else '❌ FALHOU'}")
    print(f"pgvector:     {'✅ OK' if pgvector_ok else '⚠️  NÃO INSTALADO'}")
    
    if psycopg2_ok and sqlalchemy_ok:
        print("\n🎉 Todas as conexões estão funcionando!")
        print("✨ Seu ambiente está pronto para usar LangChain com PostgreSQL!")
    else:
        print("\n❌ Algumas conexões falharam. Verifique as configurações.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
