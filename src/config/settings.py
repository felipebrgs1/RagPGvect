import os
from dotenv import load_dotenv

def load_environment_variables():
    """Carrega as variáveis de ambiente do arquivo .env."""
    load_dotenv()
    print("Variáveis de ambiente carregadas.")

def get_google_api_key() -> str:
    """Retorna a chave da API do Google Gemini."""
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")
    return key

def get_pg_connection_string() -> str:
    """Retorna a string de conexão para o PostgreSQL no formato LangChain."""
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")

    # Formato esperado pelo LangChain para PGVector com psycopg2
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

def get_pg_credentials() -> dict:
    """Retorna um dicionário com as credenciais do PostgreSQL para psycopg2 puro."""
    return {
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
        "database": os.getenv("PG_DATABASE"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASSWORD")
    }