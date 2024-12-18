from fastapi import APIRouter, HTTPException
from models.query_model import Query
from services.orchestrator import orchestrator

router= APIRouter()

@router.post("/ask_question")
async def ask(query: Query):
    """
    Endpoint to handle query requests and generate a response.

    Parameters:
    - query (Query): The query object containing the user's query string.

    Returns:
    - str: The generated response from the language model.
    """
    try:
        print("entrando a  routes")
        query_text = query.query
        if not query_text or not isinstance(query_text, str):
            raise HTTPException(status_code=400, detail="Invalid query")
        print("llamando a orquestador")
        final_response = orchestrator(query_text)
        return {"response": final_response}
    except Exception as e:
        # Raise an error for any exceptions encountered during processing
        raise HTTPException(status_code=500, detail=str(e))

