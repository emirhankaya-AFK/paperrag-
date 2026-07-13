import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routes import papers, analysis, qa, citations, reviews

app = FastAPI(
    title="PaperRAG API",
    description="Academic Research Paper Assistant Backend",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(papers.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(qa.router, prefix="/api")
app.include_router(citations.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    # Initialize local SQLite schemas
    init_db()
    print("PaperRAG database initialized successfully.")

@app.get("/")
def read_root():
    return {"message": "Welcome to PaperRAG API server."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.BACKEND_PORT, reload=True)
