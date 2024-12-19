from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from datetime import datetime

def create_chunks(text,document_name=str, category=str):
    """
    Split a text into chunks using RecursiveCharacterTextSplitter.

    Parameters:
    - text (str): text to split into chunks.
    - document_name (str): Original name of the document.
    - creation_date (str): Creation date of the document's chunk (format: YYYY-MM-DD).
    - category (str): Category of the document.

    Returns:
    - list: Dictionary of chunks with chunk_id, chunk_text, chunk_number, document_name, creation_date and category.
    """
    if not text or not isinstance(text, str):
        print("Invalid text input.")
        return []
    try:
        chunk_size=2000
        chunk_overlap=200
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_text(text)
        print(f"Text split into {len(chunks)} chunks:")

        creation_date = datetime.now().strftime("%Y-%m-%d")

        chunk_data = []
        for i, chunk in enumerate(chunks, 1):
            chunk_id = str(uuid.uuid4())
            chunk_data.append({
                "chunk_id": chunk_id,
                "chunk_text":  chunk.strip(),
                "chunk_number": i,
                "document_name": document_name,
                "creation_date":creation_date ,
                "category": category
            })
        return chunk_data
    except Exception as e:
        print(f"Error creating chunks: {e}")
        return []


