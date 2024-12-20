from fastapi.middleware.cors import CORSMiddleware

#CORS config for communicating with frontend
def cors_config(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )
