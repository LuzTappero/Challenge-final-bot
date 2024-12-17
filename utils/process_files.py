import os
from services.doc_embedding import get_embedding
from utils.chunks import create_chunks

def process_file_in_folder(folder_path: str) -> None:
    """Process all files and generate embeddings from its content."""
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a directory.")
        return

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)


def process_file(file_path: str) -> None:
    """Process a file and generate embeddings from its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except (UnicodeDecodeError, OSError) as e:
        print(f"Error reading file {file_path}: {e}")
        return

    chunks = create_chunks(content)
    if not chunks:
        print(f"File {file_path} did not produce valid chunks.")
        return
    embeddings = get_embedding(chunks)
    if embeddings:
        print(f"Embeddings generated for file: {file_path}")


#Ejemplo de ejecución

# file_path = './output/CARDILIPEN-Bisoprolol fumarato.txt'
# process_file(file_path)