import uuid
from langchain_core.documents import Document
from config.chromadb_config import chroma_config

vector_store = chroma_config()
documents = vector_store.get()

def add_embeddings_to_chroma(embeddings, chunks):
    """
    Add embeddings to Chroma vector store
    Parameters:
    embeddings(list)
    chunks(list)
    Returns:
    list: ids of added documents
    """
    documents = []
    for chunk, embeddings in zip(chunks, embeddings):
        uuids = str(uuid.uuid4())
        # Create a document with chunk text and id
        document = Document(
            page_content=chunk["chunk_text"],
            metadata={"source": chunk["chunk_id"]},
            id=uuids)
        documents.append(document)
        # Add embeddings to Chroma vector store
    try:
        ids = vector_store.add_documents(documents)
        print(f"Documents added to Chroma with IDs: {ids}")
        return ids
    except Exception as e:
        print(f"Error adding documents to Chroma: {e}")
        return []
