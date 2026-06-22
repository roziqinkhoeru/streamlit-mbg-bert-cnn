"""
pages/dashboard.py — Halaman Dashboard
Menampilkan metrik model, arsitektur, dan statistik dataset.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
from utils.styles import inject_css, section_header


def render():
    inject_css()

    # ── Hero Banner ───────────────────────────────────────────────────────────
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

    # ── Kartu Metrik Utama ────────────────────────────────────────────────────
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

        # F1 per kelas
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

        # Dataset Distribution
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

        # Confusion matrix data dari hasil penelitian
        # Rows = actual, Cols = predicted → [positive, negative, neutral]
        # TP: pos=441, neg=367, neu=331
        # Dari classification report: support pos=525, neg=417, neu=387
        # FN: pos=84, neg=50, neu=56
        # FP: pos=26, neg=58, neu=106
        cm = np.array([
            [441,  37,  47],   # actual positive → pred [pos, neg, neu]
            [ 18, 367,  32],   # actual negative
            [ 17,  39, 331],   # actual neutral
        ])

        labels_cm = ["Positif", "Negatif", "Netral"]

        # Normalized version
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

    fold_data = {
        "Kondisi": ["S1 — Class Weighting", "S2 — Random Undersampling ✓"],
        "F1-Macro (mean)": ["0.8394", "0.8461"],
        "F1 Std": ["± 0.0143", "± 0.0155"],
        "Accuracy": ["0.8423", "0.8487"],
    }

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
