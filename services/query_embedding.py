from fastapi import HTTPException
from dotenv import load_dotenv
from config.cohere_config import cohere_config

load_dotenv()
co = cohere_config()

def create_query_embedding(query: str) -> list:
    """
    Create embeddings for a given query.

    Parameters:
    query (str): The query string to create embeddings for.

    Returns:
    list: A list of floats representing the embeddings for the query.

    Raises:
    HTTPException: If no embeddings were returned for the query or if an
        error occurred while creating embeddings.
    """
    try:
        # Call the Cohere API to generate embeddings for the query
        response = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query",
            embedding_types=["float"],
        ).embeddings.float_

        # Validate the response from Cohere
        if not response or len(response) == 0:
            raise HTTPException(status_code=400, detail="No embeddings were returned for the query.")
        query_embedding = response
        if query_embedding:
            return query_embedding
    except Exception as e:
        # Catch any exceptions that occur while creating embeddings
        print("Error creating embeddings for query.")
        raise HTTPException(status_code=500, detail=f"Error creating embeddings for query: {e}")
