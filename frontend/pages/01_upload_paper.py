import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/api"

st.title("📂 Upload & Library Manager")

# Upload Form
with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Select a Research Paper (PDF)", type=["pdf"])
    submit_btn = st.form_submit_button("Upload and Process Paper")
    
    if submit_btn and uploaded_file:
        with st.spinner("Uploading and starting background processing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                res = requests.post(f"{API_URL}/papers/upload", files=files)
                if res.status_code == 200:
                    st.success("Successfully uploaded! Processing in progress. It will appear in the library shortly.")
                else:
                    st.error(f"Failed to upload: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

# Library Management
st.write("---")
st.markdown("### 📚 Current Papers Library")

try:
    res = requests.get(f"{API_URL}/papers/")
    if res.status_code == 200:
        papers = res.json()
        if not papers:
            st.info("No papers indexed yet.")
        else:
            for p in papers:
                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    st.markdown(f"**{p['title']}**")
                    st.caption(f"Authors: {', '.join(p['authors'])}")
                with col2:
                    st.caption(f"Published: {p.get('pub_date') or 'N/A'}")
                with col3:
                    if st.button("Delete 🗑️", key=p["id"]):
                        with st.spinner("Deleting..."):
                            del_res = requests.delete(f"{API_URL}/papers/{p['id']}")
                            if del_res.status_code == 200:
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error("Failed to delete.")
except Exception as e:
    st.error(f"Could not reach backend: {e}")
