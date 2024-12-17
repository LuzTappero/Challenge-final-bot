from cohere import TooManyRequestsError
from services.save_in_chromadb import add_embeddings_to_chroma
from config.cohere_config import cohere_config

co= cohere_config()

def get_embedding(chunks):
    """
    Create embeddings for the chunks.

    Parameters:
    chunks(list): A list of chunks to create embeddings for.

    Returns:
    list: A list of floats representing the embeddings for the chunks.

    Raises:
    If an error occurs while creating embeddings.
    """
    if not chunks:
        print("No chunks provided to generate embeddings.")
        return
    try:
        all_embeddings = []  # List to store all embeddings
        for chunk in chunks:
            if "chunk_text" not in chunk or "chunk_id" not in chunk:
                print(f"Invalid chunk or missing 'chunk_text' or 'chunk_id': {chunk}")
                continue
            chunk_text = chunk["chunk_text"]
            chunk_id = chunk["chunk_id"]

            # Generate embeddings for the chunk
            embedding_response = co.embed(
                texts=[chunk_text],
                model="embed-multilingual-v3.0",
                input_type="search_query",
                embedding_types=["float"]
            )
            # Verify if embeddings were returned
            if not embedding_response.embeddings:
                print(f"No embeddings were returned for chunk {chunk_id}.")
                continue
            embeddings = embedding_response.embeddings.float_
            # Add embeddings to the list
            all_embeddings.extend(embeddings)

        # Add embeddings to Chroma
        add_embeddings_to_chroma(all_embeddings, chunks)
    except TooManyRequestsError as e:
        print(f"You have exceeded the rate limit: {e}")
    except Exception as e:
        print(f"Generation error while creating embeddings: {e}")
