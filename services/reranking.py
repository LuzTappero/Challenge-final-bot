from langchain.retrievers import ContextualCompressionRetriever
from fastapi import HTTPException
from langchain_cohere import CohereRerank
from services.save_in_chromadb import vector_store
from config.chromadb_config import chroma_config
import os
from utils.clean_result_from_search import clean_relevant_text
from utils.similarity import calculate_similarity


cohere_api_key = os.getenv("COHERE_API_KEY")

vector_store = chroma_config()

def reranked_retriever(query_text, query_embedding):
    result= vector_store.similarity_search_by_vector(embedding=query_embedding,k=5)
    rerank_model = "rerank-english-v2.0"
    reranker = CohereRerank(
        model=rerank_model,
        cohere_api_key = cohere_api_key
    )

    retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=vector_store.as_retriever(),
        compression_threshold=0.2
    )
    reranked_results = retriever.invoke(query_text)
    if not reranked_results:
        raise HTTPException(status_code=404, detail="No results found")
    results = reranked_results
    results = results[0].page_content.strip()

    similitud = calculate_similarity(query_text, results)
    if similitud is not None:
        print(similitud)

    clean_information = clean_relevant_text(results)
    if clean_information is not None:
        return clean_information




