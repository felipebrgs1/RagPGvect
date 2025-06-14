from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ..config.settings import get_google_api_key

_embedding_model = None

def get_gemini_embeddings():
    """
    Retorna uma instância singleton de GoogleGenerativeAIEmbeddings.
    Usa o modelo 'models/embedding-001' que é otimizado para embeddings.
    """
    global _embedding_model
    if _embedding_model is None:
        api_key = get_google_api_key()
        _embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", # Modelo específico para embeddings do Gemini
            google_api_key=api_key
        )
        print("Modelo de embedding Gemini inicializado.")
    return _embedding_model