import streamlit as st
from typing import Dict, Any

class SummaryFormatter:
    @staticmethod
    def render_summary_card(summary: Dict[str, Any]):
        """
        Renders the structured summary.
        """
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h3 style="color: #6366f1; margin-top: 0;">Executive Summary</h3>
            <p style="font-size: 15px; line-height: 1.6; color: #cbd5e1;">{summary.get('executive_summary', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.3); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
                <h4 style="color: #a855f7; margin-top: 0;">❓ Core Problem</h4>
                <p style="color: #cbd5e1; font-size: 14px;">{summary.get('problem', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.3); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
                <h4 style="color: #10b981; margin-top: 0;">💡 Proposed Solution</h4>
                <p style="color: #cbd5e1; font-size: 14px;">{summary.get('solution', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.3); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
                <h4 style="color: #3b82f6; margin-top: 0;">📊 Key Results</h4>
                <p style="color: #cbd5e1; font-size: 14px;">{summary.get('results', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.3); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
                <h4 style="color: #f59e0b; margin-top: 0;">🚀 Broader Impact</h4>
                <p style="color: #cbd5e1; font-size: 14px;">{summary.get('impact', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.markdown("### 📌 Key Takeaways")
        for take in summary.get("key_takeaways", []):
            st.markdown(f"- {take}")

    @staticmethod
    def render_extraction_card(extraction: Dict[str, Any]):
        """
        Renders the scientific extraction.
        """
        st.markdown(f"""
        <div style="border-left: 4px solid #6366f1; padding-left: 16px; margin-bottom: 24px;">
            <h3 style="color: #fff; margin: 0 0 4px 0;">{extraction.get('title')}</h3>
            <p style="color: #94a3b8; font-size: 14px; margin: 0;"><strong>Authors:</strong> {extraction.get('authors')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🛠️ Methodology")
        st.info(extraction.get("methodology"))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌟 Key Contributions")
            for c in extraction.get("key_contributions", []):
                st.markdown(f"✅ {c}")
        with col2:
            st.markdown("#### ⚠️ Limitations")
            for l in extraction.get("limitations", []):
                st.markdown(f"❌ {l}")
                
        st.markdown("#### 📈 Main Findings")
        for res in extraction.get("main_results", []):
            st.markdown(f"🔹 {res}")
