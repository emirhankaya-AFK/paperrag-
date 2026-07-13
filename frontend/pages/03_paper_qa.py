import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/api"

st.title("💬 Research Q&A Assistant")

try:
    papers_res = requests.get(f"{API_URL}/papers/")
    papers = papers_res.json() if papers_res.status_code == 200 else []
except Exception:
    papers = []

if not papers:
    st.info("No papers available. Please upload a paper first.")
else:
    paper_options = {p["title"]: p["id"] for p in papers}
    selected_title = st.selectbox("Select Paper to Query", list(paper_options.keys()))
    selected_id = paper_options[selected_title]
    
    st.markdown("#### Ask questions about methodology, results, dataset sizes, or limitations:")
    
    question = st.text_input("Enter your research question:", placeholder="e.g., What datasets were used for training? What are the key limitations?")
    
    if st.button("Submit Question") and question:
        with st.spinner("Analyzing paper text and querying RAG database..."):
            try:
                res = requests.post(f"{API_URL}/qa/{selected_id}/ask", json={"question": question})
                if res.status_code == 200:
                    data = res.json()
                    st.write("")
                    st.markdown("### 🤖 Answer")
                    st.markdown(f'<div style="background: rgba(30, 41, 59, 0.35); border-radius: 12px; padding: 20px; border-left: 4px solid #10b981; color: #f1f5f9; line-height: 1.6;">{data["answer"]}</div>', unsafe_allow_html=True)
                    
                    st.write("")
                    st.markdown("### 📋 Evidence Sources")
                    for idx, src in enumerate(data.get("sources", [])):
                        st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.2); border: 1px solid rgba(255,255,255,0.04); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                                <strong style="color: #6366f1;">Source #{idx+1}: {src['section'].upper()}</strong>
                                <span style="color: #10b981; font-weight: bold;">Score: {src['score']:.2f}</span>
                            </div>
                            <p style="font-size: 13px; color: #cbd5e1; font-style: italic; margin: 0;">"... {src['snippet']} ..."</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Error generating answer.")
            except Exception as e:
                st.error(f"Failed to fetch answer: {e}")
