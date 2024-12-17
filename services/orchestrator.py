from fastapi import HTTPException
from models.query_model import Query
from services.response_with_db import generate_response_with_db
from config.chromadb_config import chroma_config
from services.query_embedding import create_query_embedding
from services.response_without_db import generate_response_without_db
import re

vector_store = chroma_config()

def orchestrator(query: Query):
    """
    Orchestrator function to handle query requests and generate a response.
    Parameters:
    - query (str): The query text to be processed.
    Returns:
    - str: The generated response from the language model.
    """
    try:
        query_text = query.query
        if not query_text or not isinstance(query_text, str):
            raise HTTPException(status_code=400, detail="Invalid query")

            # Lista de saludos
        greetings = ["hola", "como estás?", "qué tal?", "buenas!", "saludos"]
        user_info_queries = ["¿quién soy?", "información de usuario"]

        if query_text.lower() in greetings:
            return "¡Hola! En qué puedo ayudarte? Solo tengo información sobre medicamentos. ¿Qué deseas saber?"
        if query_text.lower() in user_info_queries:
            response = generate_response_without_db(query_text)
            return response

        query_embedding = create_query_embedding(query_text)
        results = vector_store.similarity_search_by_vector(
            embedding=query_embedding,
            k=1
        )
        if not results:
            raise HTTPException(status_code=404, detail="No results found")

        relevant_text = results[0].page_content.strip()


        cleaned_and_relevant_text = relevant_text.replace("\n", " ")
        cleaned_and_relevant_text = relevant_text.lower()
        cleaned_and_relevant_text = re.sub(r'(\d+\.\d+|\d+)\s*(mg|g|ml|cm|L|u)', r'\1 \2',relevant_text)
        cleaned_and_relevant_text = re.sub(r'[^A-Za-z0-9\s\.\-\,\(\)\%]', '',relevant_text)

        # print (f"relevante text {relevant_text}")

        final_response = generate_response_with_db(cleaned_and_relevant_text, query_text)
        return final_response
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        raise HTTPException(status_code=500, detail="Error al generar la respuesta")




