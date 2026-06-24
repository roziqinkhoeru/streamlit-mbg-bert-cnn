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

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.styles import inject_css
from pages import prediksi, tentang

# ── Inject CSS global ─────────────────────────────────────────────────────────
inject_css()

# ── Sidebar — branding (tampil di atas menu navigasi) ────────────────────────
with st.sidebar:
    st.markdown("**MBG Sentiment Analysis**")
    st.caption("IndoBERT-CNN Dual-Path")

# ── Navigasi native Streamlit ─────────────────────────────────────────────────
# Menggunakan st.navigation() agar Streamlit tidak lagi auto-generate menu
# dari folder pages/ secara terpisah (yang menyebabkan sidebar terduplikasi).
pg = st.navigation(
    [
        st.Page(prediksi.render, title="Home", url_path="home", default=True),
        st.Page(tentang.render, title="Tentang", url_path="tentang"),
    ]
)

# ── Sidebar — footer info (tampil di bawah menu navigasi) ────────────────────
with st.sidebar:
    st.divider()
    st.caption("F1-Macro 0.8547 · Akurasi 85.70%")
    st.caption("Skripsi Informatika · 2026")

pg.run()
