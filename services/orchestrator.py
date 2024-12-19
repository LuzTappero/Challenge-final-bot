from fastapi import HTTPException
from config.chromadb_config import chroma_config
from services.handle_predefined_queries import handle_predefined_queries
from services.response_lang_co import generate_response_with_db_langchain
from services.reranking import reranked_retriever

vector_store = chroma_config()

def orchestrator (query_text):
    """
    Orchestrator function to handle query requests and generate a response.
    Parameters:
    - query (str): The query text to be processed.
    Returns:
    - str: The generated response from the language model.
    """
    try:
        predefined_response = handle_predefined_queries(query_text)
        if predefined_response:
            return predefined_response
        else:
            relevant_text = reranked_retriever(query_text)
            final_response = generate_response_with_db_langchain(relevant_text, query_text)
            return final_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la respuesta: {e}")