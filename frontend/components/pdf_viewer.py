import streamlit as st
import base64
from pathlib import Path

class PDFViewerComponent:
    @staticmethod
    def render_pdf(file_path: str):
        """
        Embeds a local PDF file as an iframe inside Streamlit using base64 encoding.
        """
        path = Path(file_path)
        if not path.exists():
            st.error("PDF file path does not exist.")
            return
            
        try:
            with open(path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load PDF view directly: {e}. Fallback to text browser.")
