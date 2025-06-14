from src.config.settings import load_environment_variables
from src.database.pg_utils import setup_database_and_extension
from src.vector_store.pg_vector_store import add_documents_to_pgvector, search_pgvector
from langchain_core.documents import Document

def main():
    # 1. Carregar variáveis de ambiente
    load_environment_variables()

    # 2. Configurar o banco de dados e a extensão pgvector
    print("\n--- Configurando Banco de Dados e PGVector ---")
    setup_database_and_extension()

    # 3. Adicionar alguns documentos de exemplo
    print("\n--- Adicionando Documentos de Exemplo ---")
    
    # Criar LangChain Document objects
    sample_documents = [
        Document(
            page_content="O Brasil é um país da América do Sul conhecido por sua vasta floresta amazônica.",
            metadata={"source": "wikipedia", "category": "geography"}
        ),
        Document(
            page_content="Brasília é a capital federal do Brasil, planejada por Lúcio Costa e Oscar Niemeyer.",
            metadata={"source": "wikipedia", "category": "geography", "year": 1960}
        ),
        Document(
            page_content="A inteligência artificial (IA) é um campo da ciência da computação dedicado a criar máquinas que simulam a inteligência humana.",
            metadata={"source": "tech_blog", "category": "AI"}
        ),
        Document(
            page_content="LangChain é um framework de código aberto para desenvolver aplicações baseadas em modelos de linguagem grandes (LLMs).",
            metadata={"source": "langchain_docs", "category": "LLM_framework"}
        ),
        Document(
            page_content="PGVector é uma extensão PostgreSQL que permite armazenar embeddings de vetores e realizar buscas de similaridade eficiente.",
            metadata={"source": "pgvector_docs", "category": "database", "tech": "PostgreSQL"}
        )
    ]
    
    add_documents_to_pgvector(sample_documents, collection_name="meus_docs_teste")

    # 4. Realizar uma busca por similaridade
    print("\n--- Realizando Busca por Similaridade ---")
    query1 = "Qual é a capital do Brasil?"
    retrieved_docs1 = search_pgvector(query1, k=2, collection_name="meus_docs_teste")

    print(f"\nResultados para a query: '{query1}'")
    for i, doc in enumerate(retrieved_docs1):
        print(f"  Documento {i+1}:")
        print(f"    Conteúdo: {doc.page_content[:100]}...") # Limita para não poluir o console
        print(f"    Metadata: {doc.metadata}")
        print("-" * 30)

    query2 = "O que é LangChain?"
    retrieved_docs2 = search_pgvector(query2, k=1, collection_name="meus_docs_teste")
    
    print(f"\nResultados para a query: '{query2}'")
    for i, doc in enumerate(retrieved_docs2):
        print(f"  Documento {i+1}:")
        print(f"    Conteúdo: {doc.page_content[:100]}...")
        print(f"    Metadata: {doc.metadata}")
        print("-" * 30)

if __name__ == "__main__":
    main()