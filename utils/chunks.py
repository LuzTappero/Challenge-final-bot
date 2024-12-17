from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

def create_chunks(text, chunk_size=2000,  chunk_overlap=200):
    if not text or not isinstance(text, str):
        print("Invalid text input.")
        return []
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_text(text)
        print(f"Text split into {len(chunks)} chunks:")

        chunk_data = []
        for i, chunk in enumerate(chunks, 1):
            chunk_id = str(uuid.uuid4())
            chunk_data.append({
                "chunk_id": chunk_id,
                "chunk_text":  chunk.strip(),
                "chunk_number": i
            })
        return chunk_data
    except Exception as e:
        print(f"Error creating chunks: {e}")
        return []


