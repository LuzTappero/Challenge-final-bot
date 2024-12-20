from langchain.retrievers import ContextualCompressionRetriever
from fastapi import HTTPException
from langchain_cohere import CohereRerank
from config.chromadb_config import chroma_config
import os
from utils.clean_result_from_search import clean_relevant_text


cohere_api_key = os.getenv("COHERE_API_KEY")
vector_store = chroma_config()

def reranked_retriever(query_text):
    """
    Function to perform reranking(CohereRerank) on search results from the vector store(Chromadb).
    Parameters:
    query_text (str): The text to search for.
    Returns:
    str: The cleaned relevant text from the search results.
    """
    # Get the reranking model from Cohere
    reranker = CohereRerank(
        model= "rerank-english-v2.0",
        cohere_api_key = cohere_api_key
    )
    # Create a ContextualCompressionRetriever that uses the reranker as the base compressor
    retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=vector_store.as_retriever(),
        compression_threshold=0.6,
        search_kwargs={'k': 3}
    )

    # Get the reranked results from the retriever
    reranked_results = retriever.invoke(query_text)
    if not reranked_results:
        raise HTTPException(status_code=404, detail="Lo siento, no poseo información relevante en mi base de datos para responder tu consulta.")

    result = reranked_results[0]
    relevance_score = result.metadata['relevance_score']
    document_name = result.metadata['document_name']
    category_drug = result.metadata['category']
    creation_date = result.metadata['creation_date']

    if relevance_score>0.5:
        grounding_message = (
            f"------------------------------------------------------------------\n"
            f"El documento más relevante se obtuvo del archivo'{document_name}', perteneciente a la categoria de farmacos de {category_drug} "
            f"cargado el {creation_date}, con una puntuación de relevancia de {relevance_score:.2f}.\n"
            f"------------------------------------------------------------------\n"
            )
        print(grounding_message)
    else:
        return {
            "status_code": 404,
            "message": "Lo siento, no poseo información relevante en mi base de datos para responder tu consulta."
        }

    results_content = result.page_content.strip()
    clean_information = clean_relevant_text(results_content)
    if clean_information is not None:
        return clean_information
    else:
        return {
                "status": "error",
                "message": "Lo siento, no poseo información relevante en mi base de datos para responder tu consulta."
            }