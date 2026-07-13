# PaperRAG - Academic Research Paper Assistant Agent

PaperRAG is a complete, publication-grade Retrieval-Augmented Generation (RAG) system built to parse complex academic PDFs, analyze methodology, extract key contributions, build citation networks, query papers semantically, and compile synthesized literature reviews.

---

## Tech Stack
- **Backend API**: FastAPI + Uvicorn
- **RAG & Embeddings**: ChromaDB + Gemini Embeddings (`models/embedding-001`)
- **LLM**: Gemini API (`gemini-2.0-flash`)
- **PDF Parser**: PyMuPDF (`fitz`) with column sorting heuristics
- **Citation API**: Semantic Scholar API integration (with mock fallback)
- **Frontend Dashboard**: Streamlit

---

## Directory Structure
```
paperrag/
├── backend/
│   ├── main.py              # FastAPI server entrypoint
│   ├── db.py                # SQLite database helper
│   ├── routes/              # FastAPI router endpoints
│   ├── agents/              # Custom LLM agents
│   ├── services/            # PDF, LLM, RAG, Semantic Scholar, Plotly services
│   ├── models/              # Pydantic schemas
│   └── config/              # Prompts, keywords, settings
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── pages/               # Sidebar subpages
│   └── components/          # Plotly graph, summary cards, PDF frame
├── tests/
│   ├── generate_test_pdf.py # Test PDF program
│   ├── test_extraction.py   # PDF & meta test
│   ├── test_qa.py           # RAG Q&A test
│   └── test_citations.py   # Citation resolution test
├── requirements.txt
└── README.md
```

---

## Installation & Setup

1. **Install Python Dependencies**:
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Gemini Credentials**:
   Get an API key from Google AI Studio and set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   *Note: If no API key is set, the application will run in mock mode with pre-baked responses for offline testing.*

---

## Running the Application

### 1. Launch FastAPI Backend
```bash
python -m backend.main
```
The backend API server will run at `http://127.0.0.1:8001`. You can view the OpenAPI documentation at `http://127.0.0.1:8001/docs`.

### 2. Launch Streamlit Frontend
```bash
streamlit run frontend/app.py
```
The Streamlit app will launch at `http://localhost:8501`.

---

## Running Automated Tests
Run the test suite using `pytest`:
```bash
pytest tests/
```
