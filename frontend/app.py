import streamlit as st
import requests

# Base configurations
API_URL = "http://127.0.0.1:8001/api"

st.set_page_config(
    page_title="PaperRAG - Academic Research Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Academic Look & Feel
st.markdown("""
<style>
    /* Main background and font settings */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161a24 100%);
        color: #e2e8f0;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    /* Premium Title styling */
    h1 {
        background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Card design */
    .paper-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .paper-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Badge styling */
    .badge {
        background-color: rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 PaperRAG")
st.subheader("Your AI-Powered Academic Research Suite")

st.markdown("""
Welcome to **PaperRAG**! This advanced RAG system parses complex academic papers, extracts structured methodologies, results, and limitations, creates interactive summaries, and maps citation networks.

### Features Available:
1. **Upload Papers**: Upload your ArXiv or journal PDFs.
2. **Paper Summary**: Structured breakdowns (Problem $\\rightarrow$ Solution $\\rightarrow$ Impact).
3. **Paper Q&A**: Domain-specific Q&A citing paper sections.
4. **Citation Network**: Visualization of paper dependencies.
5. **Related Papers**: Automated suggestions from Semantic Scholar.
6. **Literature Review**: Compile summaries across 5-10 papers on any topic.
""")

# Show loaded papers summary stats
try:
    response = requests.get(f"{API_URL}/papers/")
    if response.status_code == 200:
        papers = response.json()
        st.markdown(f"### 📂 Uploaded Library ({len(papers)} papers)")
        if not papers:
            st.info("No papers uploaded yet. Go to **Upload Paper** in the sidebar to get started.")
        else:
            cols = st.columns(3)
            for idx, p in enumerate(papers):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="paper-card">
                        <h4 style="margin: 0 0 8px 0; color: #fff;">{p['title']}</h4>
                        <p style="font-size: 13px; color: #94a3b8; margin: 0 0 12px 0;"><strong>Authors:</strong> {", ".join(p['authors'][:3])}</p>
                        <span class="badge">Year: {p.get('pub_date') or 'N/A'}</span>
                        <span class="badge">ID: {p['id'][:8]}</span>
                    </div>
                    """, unsafe_allow_html=True)
except Exception as e:
    st.warning("Could not connect to PaperRAG backend. Make sure the FastAPI server is running on port 8001.")
