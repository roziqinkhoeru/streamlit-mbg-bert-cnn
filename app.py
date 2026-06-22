"""
app.py — Entry point aplikasi demo MBG Sentiment Analysis
Jalankan: streamlit run app.py
"""

import streamlit as st

# ── Konfigurasi halaman (HARUS di baris pertama sebelum import lain) ─────────
st.set_page_config(
    page_title="MBG Sentiment Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.styles import inject_css, section_header
from utils.predictor import load_model_and_tokenizer

# ── Inject CSS global ─────────────────────────────────────────────────────────
inject_css()

# ── Load model sekali di awal sesi ───────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_model():
    return load_model_and_tokenizer()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <div style="font-size:1.4rem; font-weight:700; color:#E8E9F3; line-height:1.2;">
                🧠 MBG Sentiment
            </div>
            <div style="font-size:0.75rem; color:#5A5C78; margin-top:0.3rem; font-weight:500; letter-spacing:0.04em; text-transform:uppercase;">
                Analisis Sentimen · IndoBERT-CNN
            </div>
        </div>
        <hr style="border:none; border-top:1px solid #252842; margin:0 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigasi",
        ["🏠  Dashboard", "🔍  Prediksi Sentimen", "ℹ️  Tentang"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="border:none; border-top:1px solid #252842; margin:0 0 1rem 0;">
        <div style="font-size:0.72rem; color:#5A5C78; line-height:1.8;">
            <div>Model: IndoBERT-CNN Dual-Path</div>
            <div>Kondisi: S2 (Random Undersampling)</div>
            <div>F1-Macro: <span style="color:#6C63FF; font-weight:600;">0.8547</span></div>
            <div>Accuracy: <span style="color:#6C63FF; font-weight:600;">85.70%</span></div>
        </div>
        <div style="margin-top:1.5rem; font-size:0.65rem; color:#3A3C58;">
            Skripsi · Informatika · 2026
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Routing halaman ───────────────────────────────────────────────────────────
if "Dashboard" in page:
    from pages.dashboard import render
    render()
elif "Prediksi" in page:
    from pages.prediksi import render
    render()
elif "Tentang" in page:
    from pages.tentang import render
    render()
