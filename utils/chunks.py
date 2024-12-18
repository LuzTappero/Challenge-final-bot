from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from datetime import datetime

def create_chunks(text,document_name=str, category=str):
    """
    Divide un texto en chunks con metadata adicional.

    Parameters:
    - text (str): El texto que se va a dividir.
    - chunk_size (int): Tamaño máximo de cada chunk.
    - chunk_overlap (int): Cantidad de texto que se solapa entre chunks.
    - document_name (str): Nombre del documento original.
    - creation_date (str): Fecha de creación del documento (formato: YYYY-MM-DD).
    - category (str): Categoría asociada al contenido del documento.

    Returns:
    - list: Lista de diccionarios con chunks y su metadata.
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


