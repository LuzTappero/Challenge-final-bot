from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings

PERSISTENT_DIRECTORY = "../MedicaBOTChromadb"
COLLECTION_NAME = "medications_collection"


def chroma_config():
    vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=CohereEmbeddings(model="embed-multilingual-v3.0"),
    persist_directory=PERSISTENT_DIRECTORY,
    )
    return vector_store