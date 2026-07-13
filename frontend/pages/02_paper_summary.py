import streamlit as st
import requests
from components.summary_formatter import SummaryFormatter

API_URL = "http://127.0.0.1:8001/api"

st.title("📄 Interactive Paper Summary")

# Retrieve papers
try:
    papers_res = requests.get(f"{API_URL}/papers/")
    papers = papers_res.json() if papers_res.status_code == 200 else []
except Exception:
    papers = []

if not papers:
    st.info("Please upload a paper first to view summaries.")
else:
    paper_options = {p["title"]: p["id"] for p in papers}
    selected_title = st.selectbox("Select Paper", list(paper_options.keys()))
    selected_id = paper_options[selected_title]
    
    tab1, tab2 = st.tabs(["💡 Executive Summary", "🔬 Scientific Extraction"])
    
    with tab1:
        with st.spinner("Fetching executive summary..."):
            try:
                summary_res = requests.get(f"{API_URL}/analysis/{selected_id}/summary")
                if summary_res.status_code == 200:
                    SummaryFormatter.render_summary_card(summary_res.json())
                else:
                    st.warning("Summary not ready yet. The paper is likely still processing.")
            except Exception as e:
                st.error(f"Error fetching summary: {e}")
                
    with tab2:
        with st.spinner("Fetching analytical extraction..."):
            try:
                ext_res = requests.get(f"{API_URL}/analysis/{selected_id}/extraction")
                if ext_res.status_code == 200:
                    SummaryFormatter.render_extraction_card(ext_res.json())
                else:
                    st.warning("Extraction data not ready yet. Please wait a moment.")
            except Exception as e:
                st.error(f"Error fetching extraction: {e}")
