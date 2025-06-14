from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document # Para tipagem
from ..config.settings import get_pg_connection_string
from ..embeddings.gemini_embeddings import get_gemini_embeddings

_pg_vector_store_instance = {} # Usar um dict para suportar múltiplas coleções

def get_pg_vector_store(collection_name: str = "rag_documents"):
    """
    Retorna uma instância singleton de PGVector para uma dada coleção.
    """
    if collection_name not in _pg_vector_store_instance:
        connection_string = get_pg_connection_string()
        embeddings = get_gemini_embeddings()

        _pg_vector_store_instance[collection_name] = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
            # pre_delete_collection=True # Descomente ISSO para apagar a coleção a cada execução (CUIDADO!)
            pre_delete_collection=False # Mantenha False em produção para não perder dados
        )
        print(f"PGVector store para coleção '{collection_name}' inicializado.")
    return _pg_vector_store_instance[collection_name]

def add_documents_to_pgvector(
    documents: list[Document],
    collection_name: str = "rag_documents"
):
    """
    Adiciona uma lista de documentos (LangChain Document objects) ao PGVector.
    """
    vector_store = get_pg_vector_store(collection_name)
    vector_store.add_documents(documents)
    print(f"Adicionados {len(documents)} documentos à coleção '{collection_name}'.")

def search_pgvector(
    query: str,
    k: int = 5,
    collection_name: str = "rag_documents"
) -> list[Document]:
    """
    Realiza uma busca por similaridade no PGVector.
    """
    vector_store = get_pg_vector_store(collection_name)
    # A função as_retriever() já encapsula a geração do embedding da query
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    
    print(f"Buscando '{query}' na coleção '{collection_name}'...")
    relevant_docs = retriever.invoke(query)
    print(f"Encontrados {len(relevant_docs)} documentos relevantes.")
    return relevant_docs