"""
pages/tentang.py — Halaman Tentang (About)
Informasi peneliti, penelitian, dataset, dan referensi.
"""

import streamlit as st
from utils.styles import inject_css, section_header


def render():
    inject_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-badge">ℹ️ Tentang Penelitian</div>
            <div class="hero-title">Analisis Sentimen MBG<br>
                <span style="color:#6C63FF;">Menggunakan BERT-CNN</span>
            </div>
            <div class="hero-subtitle">
                Tugas Akhir · Program Studi Informatika · 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Profil Peneliti ───────────────────────────────────────────────────────
    col_profil, col_abstrak = st.columns([1, 1.8])

    with col_profil:
        section_header("Peneliti", "👤")
        info_items = {
            "Nama": "Khoeru Roziqin",
            "Program Studi": "Informatika",
            "Jenjang": "Strata 1 (S1)",
            "Tahun": "2026",
            "Topik": "Sentiment Analysis · NLP · Deep Learning",
        }
        for k, v in info_items.items():
            st.markdown(
                f"""
                <div style="padding:0.5rem 0; border-bottom:1px solid #252842;">
                    <div style="font-size:0.68rem; color:#5A5C78; text-transform:uppercase;
                                letter-spacing:0.06em; margin-bottom:0.15rem;">{k}</div>
                    <div style="font-size:0.88rem; color:#E8E9F3; font-weight:500;">{v}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        section_header("Judul Skripsi", "📄")
        st.markdown(
            """
            <div style="background:#141627; border:1px solid #252842; border-left:3px solid #6C63FF;
                        border-radius:8px; padding:1rem; font-size:0.85rem; color:#E8E9F3;
                        line-height:1.6; font-style:italic;">
                "Analisis Sentimen Opini Publik di Platform X Mengenai Program Makan Bergizi Gratis
                Menggunakan BERT-CNN"
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_abstrak:
        section_header("Abstrak Penelitian", "📝")
        st.markdown(
            """
            <div style="font-size:0.88rem; color:#9899B0; line-height:1.8; text-align:justify;">
                Penelitian ini mengembangkan sistem analisis sentimen untuk mengklasifikasikan opini
                publik di platform X (Twitter) terkait <b style="color:#E8E9F3;">Program Makan Bergizi
                Gratis (MBG)</b> — program unggulan pemerintah Indonesia yang diluncurkan pada tahun 2025.
                <br><br>
                Pendekatan yang digunakan adalah arsitektur hybrid <b style="color:#6C63FF;">IndoBERT-CNN
                Dual-Path</b> yang menggabungkan dua jalur representasi komplementer: (1) representasi
                konteks global menggunakan token [CLS] dari IndoBERT, dan (2) penangkapan pola n-gram
                lokal menggunakan CNN 1D multi-kernel. Kedua jalur digabungkan sebelum memasuki
                classifier head.
                <br><br>
                Dataset terdiri dari <b style="color:#E8E9F3;">6.642 tweet berlabel</b> yang dikumpulkan
                menggunakan TwitHarvest dengan kata kunci "mbg" dan "makan bergizi gratis" sepanjang
                periode Januari 2025 hingga Januari 2026. Klasifikasi dilakukan ke dalam tiga kelas:
                <b style="color:#10B981;">Positif</b>, <b style="color:#EF4444;">Negatif</b>, dan
                <b style="color:#F59E0B;">Netral</b>.
                <br><br>
                Model final dievaluasi menggunakan stratified 5-fold cross-validation dan menghasilkan
                <b style="color:#E8E9F3;">F1-Macro sebesar 0.8547</b> dan
                <b style="color:#E8E9F3;">Accuracy 85.70%</b> pada test set independen (1.329 tweet).
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Dataset & Metodologi ──────────────────────────────────────────────────
    col_data, col_metode = st.columns(2)

    with col_data:
        section_header("Informasi Dataset", "🗃️")

        dataset_items = [
            ("Sumber Data", "Platform X (Twitter)"),
            ("Tools Scraping", "TwitHarvest (open-source)"),
            ("Kata Kunci", '"mbg", "makan bergizi gratis"'),
            ("Periode", "Januari 2025 – Januari 2026"),
            ("Total Raw", "172.009 tweet"),
            ("Total Berlabel", "6.642 tweet"),
            ("Distribusi", "Positif: 2.625 (39.5%)"),
            ("", "Negatif: 2.085 (31.4%)"),
            ("", "Netral: 1.932 (29.1%)"),
            ("Train/Val", "5.313 tweet (80%)"),
            ("Test Set", "1.329 tweet (20%) — fixed"),
            ("Labeling", "Manual annotation"),
        ]

        for k, v in dataset_items:
            if k:
                st.markdown(
                    f"""<div style="display:flex;justify-content:space-between;align-items:flex-start;
                                  padding:0.4rem 0;border-bottom:1px solid #252842;">
                        <span style="font-size:0.78rem;color:#5A5C78;min-width:100px;">{k}</span>
                        <span style="font-size:0.78rem;color:#E8E9F3;font-weight:500;text-align:right;">{v}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""<div style="display:flex;justify-content:flex-end;padding:0.1rem 0;">
                        <span style="font-size:0.78rem;color:#E8E9F3;font-weight:500;">{v}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

    with col_metode:
        section_header("Metodologi", "⚙️")

        steps = [
            ("1", "#6C63FF", "Pengumpulan Data", "Crawling Twitter/X menggunakan TwitHarvest dengan kata kunci terkait MBG"),
            ("2", "#8B5CF6", "Preprocessing", "Cleaning, normalisasi teks, tokenisasi menggunakan IndoBERT tokenizer"),
            ("3", "#A78BFA", "Labeling", "Manual annotation: Positif / Negatif / Netral"),
            ("4", "#10B981", "Balancing", "Random Undersampling (kondisi S2 terpilih vs S1 Class Weighting)"),
            ("5", "#3B82F6", "Training", "5-Fold Stratified CV + Staged Grid Search (Phase 1, 2A, 2B, 3)"),
            ("6", "#F59E0B", "Evaluasi", "F1-Macro, Accuracy, Precision, Recall pada test set independen"),
        ]

        for num, color, title, desc in steps:
            st.markdown(
                f"""
                <div style="display:flex;gap:0.75rem;margin-bottom:0.75rem;align-items:flex-start;">
                    <div style="background:{color}20;color:{color};border:1px solid {color}50;
                                border-radius:50%;width:24px;height:24px;min-width:24px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:0.7rem;font-weight:700;">{num}</div>
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:#E8E9F3;">{title}</div>
                        <div style="font-size:0.76rem;color:#9899B0;line-height:1.5;margin-top:0.1rem;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Referensi Utama ───────────────────────────────────────────────────────
    section_header("Referensi Utama", "📚")

    references = [
        ("Devlin et al. (2019)", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Dasar arsitektur BERT yang digunakan"),
        ("Kim (2014)", "Convolutional Neural Networks for Sentence Classification", "Dasar CNN 1D untuk klasifikasi teks"),
        ("Muhabbab et al. (2025)", "Sentiment Analysis Using BERT-Based Model", "Justifikasi pendekatan BERT untuk sentimen"),
        ("Mishra et al. (2020)", "BERT-CNN: A Hybrid Model for Sentiment Analysis", "Inspirasi arsitektur hybrid BERT+CNN"),
        ("Mandhasiya et al. (2024)", "IndoBERT for Indonesian NLP Tasks", "Penggunaan IndoBERT untuk NLP Bahasa Indonesia"),
        ("Imron et al. (2023)", "Analisis Sentimen Media Sosial dengan Deep Learning", "Konteks penelitian sentimen Indonesia"),
        ("Wilie et al. (2020)", "IndoNLU: Benchmark NLU Bahasa Indonesia", "Benchmark IndoBERT"),
    ]

    col1, col2 = st.columns(2)
    for i, (author, title, note) in enumerate(references):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(
                f"""
                <div style="background:#141627;border:1px solid #252842;border-radius:8px;
                            padding:0.85rem;margin-bottom:0.6rem;">
                    <div style="font-size:0.75rem;font-weight:600;color:#6C63FF;margin-bottom:0.25rem;">{author}</div>
                    <div style="font-size:0.78rem;color:#E8E9F3;font-weight:500;line-height:1.4;margin-bottom:0.25rem;">{title}</div>
                    <div style="font-size:0.7rem;color:#5A5C78;font-style:italic;">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Tech Stack ────────────────────────────────────────────────────────────
    section_header("Tech Stack Aplikasi Demo", "🛠️")

    techs = [
        ("🐍 Python", "3.10+", "#3B82F6"),
        ("🎈 Streamlit", "≥ 1.35", "#FF4B4B"),
        ("🔥 PyTorch", "≥ 2.0", "#EF4444"),
        ("🤗 Transformers", "≥ 4.40", "#F59E0B"),
        ("🐼 Pandas", "≥ 2.0", "#10B981"),
        ("📊 Plotly", "≥ 5.18", "#6C63FF"),
    ]

    cols = st.columns(len(techs))
    for col, (name, ver, color) in zip(cols, techs):
        with col:
            st.markdown(
                f"""
                <div style="background:#141627;border:1px solid #252842;border-radius:8px;
                            padding:0.75rem;text-align:center;">
                    <div style="font-size:0.9rem;color:#E8E9F3;font-weight:600;">{name}</div>
                    <div style="font-size:0.7rem;color:{color};margin-top:0.2rem;font-family:'JetBrains Mono',monospace;">{ver}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="margin-top:2rem; padding:1rem; background:#141627; border:1px solid #252842;
                    border-radius:8px; font-size:0.75rem; color:#5A5C78; text-align:center;">
            Aplikasi demo ini dikembangkan sebagai artefak pendukung sidang skripsi dan dokumentasi HKI.
            Model: <span style="color:#6C63FF; font-family:'JetBrains Mono',monospace;">indobert_cnn_dualpath_S2.pt</span>
            · Dibuat dengan ❤️ menggunakan Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
