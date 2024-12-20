import os
from services.get_docs_embedding import get_embedding
from utils.create_chunks import create_chunks

def process_file(file_path: str) -> None:
    """Process a file and generate embeddings from its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            file_title = file.name.split("/")[-1].split(".")[0]  # Lee el título del documento
    except (UnicodeDecodeError, OSError) as e:
        print(f"Error reading file {file_path}: {e}")
        return
    # Process the file and generate chunks
    chunks = create_chunks(content, file_title, category="Medicamentos Cardiovasculares")
    if not chunks:
        print(f"File {file_path} did not produce valid chunks.")
        return
    # Generate embeddings
    embeddings = get_embedding(chunks)
    if embeddings:
        print(f"Embeddings generated for file: {file_path}")


# Example usage
# file_path = './output/CARDILIPEN-Bisoprolol fumarato.txt'
# process_file(file_path)