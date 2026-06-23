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
from pages import dashboard, prediksi, tentang

# ── Inject CSS global ─────────────────────────────────────────────────────────
inject_css()

# ── Sidebar — branding (tampil di atas menu navigasi) ────────────────────────
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

# ── Navigasi native Streamlit ─────────────────────────────────────────────────
# Menggunakan st.navigation() agar Streamlit tidak lagi auto-generate menu
# dari folder pages/ secara terpisah (yang menyebabkan sidebar terduplikasi).
pg = st.navigation(
    [
        st.Page(dashboard.render, title="Dashboard", icon="🏠", url_path="dashboard", default=True),
        st.Page(prediksi.render, title="Prediksi Sentimen", icon="🔍", url_path="prediksi"),
        st.Page(tentang.render, title="Tentang", icon="ℹ️", url_path="tentang"),
    ]
)

# ── Sidebar — footer info (tampil di bawah menu navigasi) ────────────────────
with st.sidebar:
    st.markdown(
        """
        <hr style="border:none; border-top:1px solid #252842; margin:1rem 0 1rem 0;">
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

pg.run()
