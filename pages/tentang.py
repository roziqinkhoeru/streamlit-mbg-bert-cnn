"""
pages/tentang.py — Halaman Tentang
Project showcase: ringkasan penelitian, performa model, arsitektur,
dataset, metodologi, referensi, dan tech stack. Menggabungkan halaman
Dashboard (metrik & arsitektur) dengan halaman Tentang (profil & referensi)
menjadi satu halaman portofolio proyek.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.styles import inject_css, section_header


def render():
    inject_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-badge">⚡ Demo Sidang Skripsi · 2026</div>
            <div class="hero-title">
                Analisis Sentimen Opini Publik<br>
                <span style="color:#6C63FF;">Program Makan Bergizi Gratis (MBG)</span>
            </div>
            <div class="hero-subtitle">
                Model hybrid IndoBERT-CNN Dual-Path untuk klasifikasi sentimen tiga kelas
                pada data Twitter/X berbahasa Indonesia. Dataset: 6.642 tweet · Periode: Jan 2025 – Jan 2026.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Highlight Strip — ringkasan cepat untuk pembaca yang scroll sekilas ────
    h1, h2, h3, h4 = st.columns(4)
    for col, label, value in [
        (h1, "Accuracy", "85.70%"),
        (h2, "F1-Macro", "0.8547"),
        (h3, "Dataset", "6.642 tweet"),
        (h4, "Kelas", "3 (Pos/Neg/Netral)"),
    ]:
        with col:
            st.markdown(
                f"""<div class="metric-card" style="text-align:center; padding:0.9rem 0.5rem;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value metric-accent" style="font-size:1.5rem;">{value}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Profil & Abstrak ──────────────────────────────────────────────────────
    col_profil, col_abstrak = st.columns([1, 1.8])

    with col_profil:
        section_header("Peneliti", "👤")
        with st.container(border=True):
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
                    <div style="padding:0.4rem 0; border-bottom:1px solid #252842;">
                        <div style="font-size:0.68rem; color:#5A5C78; text-transform:uppercase;
                                    letter-spacing:0.06em; margin-bottom:0.15rem;">{k}</div>
                        <div style="font-size:0.88rem; color:#E8E9F3; font-weight:500;">{v}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="font-size:0.68rem; color:#5A5C78; text-transform:uppercase;
                            letter-spacing:0.06em; margin-bottom:0.4rem;">Judul Skripsi</div>
                <div style="font-size:0.85rem; color:#E8E9F3; line-height:1.6; font-style:italic;
                            border-left:3px solid #6C63FF; padding-left:0.75rem;">
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

    # ── Performa Model ────────────────────────────────────────────────────────
    section_header("Performa Model pada Test Set", "📊")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">F1-Macro</div>
            <div class="metric-value metric-accent">0.8547</div>
            <div class="metric-sub">Test set · 1.329 tweet</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Accuracy</div>
            <div class="metric-value metric-accent">85.70%</div>
            <div class="metric-sub">1.139 / 1.329 benar</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Precision</div>
            <div class="metric-value">0.8551</div>
            <div class="metric-sub">Macro average</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Recall</div>
            <div class="metric-value">0.8585</div>
            <div class="metric-sub">Macro average</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Per-Class F1 + Confusion Matrix ──────────────────────────────────────
    col_f1, col_cm = st.columns([1, 1.6])

    with col_f1:
        section_header("F1-Score per Kelas", "🎯")

        classes = ["Positif", "Negatif", "Netral"]
        f1_vals = [0.8891, 0.8717, 0.8034]
        colors  = ["#10B981", "#EF4444", "#F59E0B"]

        for cls, f1, color in zip(classes, f1_vals, colors):
            pct = f1 * 100
            st.markdown(
                f"""
                <div class="f1-row">
                    <span class="f1-class">{cls}</span>
                    <div class="f1-bar-wrap">
                        <div class="f1-bar" style="width:{pct}%; background:{color};"></div>
                    </div>
                    <span class="f1-score" style="color:{color};">{f1:.4f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        section_header("Distribusi Dataset", "📂")
        fig_dist = go.Figure(data=[go.Pie(
            labels=["Positif", "Negatif", "Netral"],
            values=[2625, 2085, 1932],
            hole=0.55,
            marker=dict(colors=["#10B981", "#EF4444", "#F59E0B"],
                        line=dict(color="#0D0F1A", width=2)),
            textinfo="percent+label",
            textfont=dict(size=12, color="#E8E9F3"),
            hovertemplate="<b>%{label}</b><br>%{value:,} tweet<br>%{percent}<extra></extra>",
        )])
        fig_dist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=200,
            annotations=[dict(
                text="6.642<br><span style='font-size:10px'>tweet</span>",
                x=0.5, y=0.5,
                font=dict(size=16, color="#E8E9F3", family="JetBrains Mono"),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_cm:
        section_header("Confusion Matrix — Test Set", "🔢")

        cm = np.array([
            [441,  37,  47],   # actual positive → pred [pos, neg, neu]
            [ 18, 367,  32],   # actual negative
            [ 17,  39, 331],   # actual neutral
        ])

        labels_cm = ["Positif", "Negatif", "Netral"]
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

        fig_cm = go.Figure(data=go.Heatmap(
            z=cm_norm,
            x=labels_cm,
            y=labels_cm,
            colorscale=[[0, "#141627"], [0.5, "#3730A3"], [1, "#6C63FF"]],
            showscale=True,
            colorbar=dict(
                thickness=12,
                tickfont=dict(color="#9899B0", size=10),
                bgcolor="#141627",
            ),
            text=[[f"{cm_norm[i][j]:.2f}<br>({cm[i][j]})" for j in range(3)] for i in range(3)],
            texttemplate="%{text}",
            textfont=dict(size=13, color="#E8E9F3", family="JetBrains Mono"),
            hovertemplate=(
                "Aktual: <b>%{y}</b><br>"
                "Prediksi: <b>%{x}</b><br>"
                "Jumlah: <b>%{customdata}</b><extra></extra>"
            ),
            customdata=cm,
        ))
        fig_cm.update_layout(
            paper_bgcolor="#141627",
            plot_bgcolor="#141627",
            font=dict(color="#9899B0", family="Inter"),
            xaxis=dict(
                title=dict(text="Prediksi", font=dict(size=12, color="#9899B0")),
                tickfont=dict(size=12, color="#E8E9F3"),
                showgrid=False,
            ),
            yaxis=dict(
                title=dict(text="Aktual", font=dict(size=12, color="#9899B0")),
                tickfont=dict(size=12, color="#E8E9F3"),
                autorange="reversed",
                showgrid=False,
            ),
            margin=dict(t=10, b=40, l=60, r=20),
            height=320,
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        st.markdown(
            """<div style="font-size:0.72rem; color:#5A5C78; text-align:center; margin-top:-0.5rem;">
            Nilai = proporsi (jumlah absolut dalam kurung) · Diagonal = prediksi benar
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Arsitektur Model ──────────────────────────────────────────────────────
    section_header("Arsitektur Model", "🏗️")

    col_arch, col_hp = st.columns([1.4, 1])

    with col_arch:
        st.markdown(
            """
            <div class="arch-block">
Input Tweet → <span class="arch-highlight">IndoBERT</span> (indobert-base-p2)
                        ↓
              last_hidden_state [batch, 128, 768]
                        │
          ┌─────────────┴──────────────┐
          │                            │
   <span class="arch-highlight">Path 1: [CLS]</span>          <span class="arch-highlight">Path 2: CNN 1D</span>
   Konteks Global       N-gram Lokal [1,2,3]
   Dropout(0.1)         Filter: 256 × 3 kernels
   [batch, 768]         GlobalMaxPool
                        [batch, 768]
          │                            │
          └──────── Concatenate ───────┘
                   [batch, 1.152]
                        ↓
              Dropout(0.5) → Dense(256, ELU)
                        ↓
              Dropout(0.5) → Dense(3)
                        ↓
                    Softmax
                        ↓
          [Positif | Negatif | Netral]
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_hp:
        section_header("Hyperparameter Final", "⚙️")
        params = {
            "Backbone": "indobert-base-p2",
            "LR BERT": "1e-5",
            "LR CNN": "1e-4",
            "Batch Size": "32",
            "Weight Decay": "0.01",
            "Dropout": "0.5",
            "CNN Filter": "256",
            "N-gram": "[1, 2, 3]",
            "Dense": "256 (ELU)",
            "Max Length": "128 token",
            "Imbalance": "Random Undersampling",
            "Validasi": "5-Fold Stratified CV",
        }
        for k, v in params.items():
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:0.4rem 0; border-bottom:1px solid #252842;">
                    <span style="font-size:0.8rem; color:#9899B0;">{k}</span>
                    <span style="font-size:0.8rem; color:#E8E9F3; font-weight:500;
                                 font-family:'JetBrains Mono',monospace;">{v}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── K-Fold Summary ────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    section_header("Hasil K-Fold Cross Validation (Phase 3)", "📈")

    col_s1, col_s2 = st.columns(2)
    for col, cond, f1, std, acc, is_best in [
        (col_s1, "S1 — Class Weighting", "0.8394", "± 0.0143", "84.23%", False),
        (col_s2, "S2 — Random Undersampling", "0.8461", "± 0.0155", "84.87%", True),
    ]:
        with col:
            border = "#6C63FF" if is_best else "#252842"
            badge  = '<span class="tag tag-purple" style="margin-left:0.5rem;">✓ Terbaik</span>' if is_best else ""
            st.markdown(
                f"""
                <div class="info-card" style="border-color:{border};">
                    <div class="info-card-title">{cond}{badge}</div>
                    <div style="display:flex; gap:2rem; margin-top:0.5rem;">
                        <div>
                            <div style="font-size:0.68rem;color:#5A5C78;">F1-Macro</div>
                            <div style="font-size:1.3rem;font-weight:700;color:#6C63FF;font-family:'JetBrains Mono',monospace;">{f1}</div>
                            <div style="font-size:0.72rem;color:#9899B0;">{std}</div>
                        </div>
                        <div>
                            <div style="font-size:0.68rem;color:#5A5C78;">Accuracy</div>
                            <div style="font-size:1.3rem;font-weight:700;color:#E8E9F3;font-family:'JetBrains Mono',monospace;">{acc}</div>
                        </div>
                    </div>
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
