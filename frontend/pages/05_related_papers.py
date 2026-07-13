import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/api"

st.title("🔗 Related Papers Recommendations")

try:
    papers_res = requests.get(f"{API_URL}/papers/")
    papers = papers_res.json() if papers_res.status_code == 200 else []
except Exception:
    papers = []

if not papers:
    st.info("Please upload a paper to find related research.")
else:
    paper_options = {p["title"]: p["id"] for p in papers}
    selected_title = st.selectbox("Select Core Paper", list(paper_options.keys()))
    selected_id = paper_options[selected_title]
    
    with st.spinner("Retrieving related papers from Semantic Scholar..."):
        try:
            res = requests.get(f"{API_URL}/citations/{selected_id}/related")
            if res.status_code == 200:
                recommendations = res.json()
                
                st.write("")
                st.markdown("### 💡 Recommended Papers")
                for r in recommendations:
                    authors_list = [a.get("name", "") for a in r.get("authors", [])]
                    authors_str = ", ".join(authors_list[:3])
                    
                    st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; margin-bottom: 12px;">
                        <h4 style="margin: 0 0 6px 0; color: #fff;">{r['title']}</h4>
                        <p style="font-size: 13px; color: #94a3b8; margin: 0 0 8px 0;"><strong>Authors:</strong> {authors_str} | <strong>Venue:</strong> {r.get('venue') or 'N/A'} ({r.get('year') or 'N/A'})</p>
                        <p style="font-size: 13px; color: #cbd5e1; margin: 0 0 12px 0; line-height: 1.5;">{r.get('abstract', 'No abstract available.')[:300]}...</p>
                        <span style="background-color: rgba(16, 185, 129, 0.15); color: #34d399; padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 600;">Citations Count: {r.get('citationCount', 0)}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Error retrieving recommendations.")
        except Exception as e:
            st.error(f"Backend retrieval failed: {e}")
