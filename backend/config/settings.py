import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")
SQLITE_DB_PATH = str(DATA_DIR / "paperrag.db")

# Create directories if they do not exist
DATA_DIR.mkdir(exist_ok=True, parents=True)
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

# LLM Config
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_MODEL = "gemini-2.0-flash"

# Port configs
BACKEND_PORT = 8001
FRONTEND_PORT = 8501
