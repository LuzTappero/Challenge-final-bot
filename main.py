from fastapi import FastAPI
from routes.routes import router as api_router
from config.CORSconfig import cors_config
from config.chromadb_config import chroma_config
from utils.process_files import process_file

vector_store = chroma_config()

app = FastAPI()
cors_config(app)

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Task API!"}

