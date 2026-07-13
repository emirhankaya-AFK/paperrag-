import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go
import json

class CitationGraphComponent:
    @staticmethod
    def render_graph(graph_json_str: str):
        """
        Loads the plotly graph json and displays it in Streamlit.
        """
        try:
            fig_data = json.loads(graph_json_str)
            fig = go.Figure(fig_data)
            
            # Update look/feel for streamlit integration
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to render citation network: {e}")
