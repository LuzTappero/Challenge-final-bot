from dotenv import load_dotenv
import cohere
import os
from langchain_cohere import CohereEmbeddings

load_dotenv()

def cohere_config():
    try:
        #Get the cohere api key
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY is not set at .env")

        embeddings_function = CohereEmbeddings(
            model="embed-multilingual-v3.0",
            cohere_api_key=cohere_api_key
        )
        #Initialize the cohere client
        co = cohere.ClientV2(cohere_api_key)
        return co

    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise
