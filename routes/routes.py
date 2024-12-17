from fastapi import APIRouter, HTTPException
from config.chromadb_config import chroma_config
from models.query_model import Query
from services.orchestrator import orchestrator
from typing import List

router= APIRouter()

vector_store = chroma_config()


@router.post("/ask_question")
async def ask(query: Query):
    """
    Endpoint to handle query requests and generate a response.

    Parameters:
    - query (Query): The query object containing the user's query string.

    Returns:
    - str: The generated response from the language model.
    """
    if not query.query or not isinstance(query.query, str):
        # Raise an error if the query is invalid
        raise HTTPException(status_code=400, detail="Invalid query")
    try:
        # Llamada al orquestador
            final_response = orchestrator(query)
            return {"response": final_response}
    except Exception as e:
        # Raise an error for any exceptions encountered during processing
        raise HTTPException(status_code=500, detail=str(e))
