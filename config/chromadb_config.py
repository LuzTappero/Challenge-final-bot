from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_cohere import CohereEmbeddings

#Crear un cliente persistente en chroma
persistent_directory ="../med_collect_chroma"
collection_name = "medications_collection"
embeddings_function = CohereEmbeddings(model="embed-multilingual-v3.0")

def chroma_config():
    vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings_function,
    persist_directory=persistent_directory,
    )
    return vector_store