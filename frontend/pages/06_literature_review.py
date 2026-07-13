import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/api"

st.title("📚 Automated Literature Review Synthesis")

try:
    papers_res = requests.get(f"{API_URL}/papers/")
    papers = papers_res.json() if papers_res.status_code == 200 else []
except Exception:
    papers = []

if not papers:
    st.info("Please upload multiple papers in the library to create literature reviews.")
else:
    st.markdown("Select papers from your library and input the study topic to generate a synthesized literature report:")
    
    paper_options = {p["title"]: p["id"] for p in papers}
    selected_titles = st.multiselect("Select Papers to Synthesize", list(paper_options.keys()))
    
    topic = st.text_input("Synthesis Topic/Query:", placeholder="e.g., Attention-based Sequence Models and Translation Optimization")
    
    if st.button("Synthesize Report") and selected_titles and topic:
        selected_ids = [paper_options[t] for t in selected_titles]
        
        with st.spinner("Synthesizing paper contents and generating review..."):
            try:
                res = requests.post(f"{API_URL}/reviews/synthesize", json={
                    "paper_ids": selected_ids,
                    "topic": topic
                })
                if res.status_code == 200:
                    data = res.json()
                    st.write("---")
                    st.markdown("### 📄 Synthesized Literature Review")
                    st.markdown(data["report"])
                else:
                    st.error("Failed to generate literature review synthesis.")
            except Exception as e:
                st.error(f"Error calling review generator: {e}")
