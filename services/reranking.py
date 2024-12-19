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
    #El siguiente codigo es una herramienta que mejora la recuperacion de los docs optimizando el ranking y filtrando los resultados por relevancia
    retriever = ContextualCompressionRetriever(
        base_compressor=reranker, #Modelo de rankeo -asigna el score
        base_retriever=vector_store.as_retriever(), #componente que hace la busqueda inicial en el vector store
        compression_threshold=0.4, #define el umbral de compresion o "relevancia", auqellos menores a 0.4 se eliminan
        search_kwargs={'k': 3}
    )

    # Get the reranked results from the retriever
    #El siguiente codigo usa el retriever configurado previamente para obtener los resultados reordenados(reranked) con base en la consulta query_text. El invoke ejecuta el retriever ocn la query text
    reranked_results = retriever.invoke(query_text)
    if not reranked_results:
        raise HTTPException(status_code=404, detail="No results found")

    # Get the relevance score from the first reranked result
    result = reranked_results[0]
    #Relevancia del resultado primero
    relevance_score = result.metadata['relevance_score']

    document_name = result.metadata['document_name']
    category_drug = result.metadata['category']
    creation_date = result.metadata['creation_date']

    grounding_message = (
        f"------------------------------------------------------------------\n"
        f"El documento más relevante se obtuvo del archivo'{document_name}', perteneciente a la categoria de farmacos de {category_drug} "
        f"cargado el {creation_date}, con una puntuación de relevancia de {relevance_score:.2f}.\n"
        f"------------------------------------------------------------------\n"
        )

    # Imprimir el mensaje
    print(grounding_message)

    # Get the page content from the first reranked result and clean it

    results_content = result.page_content.strip()
    clean_information = clean_relevant_text(results_content)
    if clean_information is not None:
        return clean_information
    else:
        raise HTTPException(status_code=404, detail="Lo siento, no poseo información relevante en mi base de datos para responder tu consulta.")