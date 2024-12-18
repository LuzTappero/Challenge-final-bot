from fastapi import HTTPException
from config.chromadb_config import chroma_config
from services.query_embedding import create_query_embedding
from services.predef_response import handle_predefined_queries
from services.response_lang_co import generate_response_with_db_langchain
from services.reranking import reranked_retriever

vector_store = chroma_config()

def orchestrator(query_text):
    """
    Orchestrator function to handle query requests and generate a response.
    Parameters:
    - query (str): The query text to be processed.
    Returns:
    - str: The generated response from the language model.
    """
    try:
        print("entro a orquestador")
        predefined_response = handle_predefined_queries(query_text)
        if predefined_response:
            return predefined_response
        else:
            print("Entrando a hacer embed query")
            query_embedding = create_query_embedding(query_text)
            print("Entrando a hacer rerank")
            relevant_text = reranked_retriever(query_text, query_embedding)
            print("Entrando a hacer response")
            final_response = generate_response_with_db_langchain(relevant_text, query_text)
            return final_response
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        raise HTTPException(status_code=500, detail="Error al generar la respuesta")




