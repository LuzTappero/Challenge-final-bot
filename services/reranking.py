from langchain.retrievers import ContextualCompressionRetriever
from fastapi import HTTPException
from langchain_cohere import CohereRerank
from config.chromadb_config import chroma_config
import os
from utils.clean_result_from_search import clean_relevant_text


cohere_api_key = os.getenv("COHERE_API_KEY")
vector_store = chroma_config()

def reranked_retriever(query_text, query_embedding):
    search_results = vector_store.similarity_search_by_vector(embedding=query_embedding,k=5)
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

    result = reranked_results[0]
    relevance_score = result.metadata.get("relevance_score", None)
    print(f"Relevance score: {relevance_score}")

    results_content = reranked_results[0].page_content.strip()
    clean_information = clean_relevant_text(results_content)
    if clean_information is not None:
        return clean_information





