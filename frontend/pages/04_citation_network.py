import streamlit as st
import requests
from components.citation_graph import CitationGraphComponent

API_URL = "http://127.0.0.1:8001/api"

st.title("🕸️ Citation Network Visualization")

try:
    papers_res = requests.get(f"{API_URL}/papers/")
    papers = papers_res.json() if papers_res.status_code == 200 else []
except Exception:
    papers = []

if not papers:
    st.info("No papers indexed yet.")
else:
    paper_options = {p["title"]: p["id"] for p in papers}
    selected_title = st.selectbox("Select Paper for Citation Graph", list(paper_options.keys()))
    selected_id = paper_options[selected_title]
    
    with st.spinner("Generating network visualization..."):
        try:
            res = requests.get(f"{API_URL}/citations/{selected_id}/network")
            if res.status_code == 200:
                data = res.json()
                
                # Render plotly graph
                CitationGraphComponent.render_graph(data["graph_json"])
                
                # Show references list
                st.write("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📥 Cited By (Citing Papers)")
                    for c_title in data["network"]["cited_by"]:
                        st.markdown(f"- 📄 {c_title}")
                        
                with col2:
                    st.markdown("### 📤 Cites (References)")
                    for ref in data["network"]["references"][:10]:
                        title = ref["title"] if ref["title"] else ref["raw_text"]
                        year = f" ({ref['year']})" if ref["year"] else ""
                        authors = f" by {', '.join(ref['authors'][:2])}" if ref["authors"] else ""
                        st.markdown(f"- 📄 {title}{year}{authors}")
            else:
                st.error("Error creating citation network.")
        except Exception as e:
            st.error(f"Failed connection: {e}")
