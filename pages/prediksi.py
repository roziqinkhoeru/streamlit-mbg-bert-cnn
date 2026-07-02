"""
pages/prediksi.py — Halaman Prediksi Sentimen
Tab A: Input teks manual
Tab B: Upload CSV batch prediction
Tab C: Sample data terkurasi untuk demo cepat
"""

import html
import io

import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, render_result_card
from utils.predictor import load_model_and_tokenizer, predict_single

SAMPLE_DATA_CSV = """full_text,label
Program makan bergizi gratis sangat bermanfaat untuk anak sekolah di daerah terpencil,positive
MBG ini pemborosan anggaran negara yang tidak tepat sasaran dan tidak efisien,negative
Pemerintah meluncurkan program MBG untuk 82 juta penerima manfaat di seluruh Indonesia,neutral
Anak saya jadi lebih semangat sekolah sejak ada program makan gratis ini terima kasih pemerintah,positive
Kualitas makanan dalam program MBG sangat buruk dan tidak layak dikonsumsi anak-anak,negative
Program makan bergizi gratis mulai dilaksanakan di 26 provinsi pada Januari 2025,neutral
Luar biasa program ini bisa mengurangi stunting dan meningkatkan gizi anak bangsa Indonesia,positive
Anggaran MBG sebesar 71 triliun rupiah sangat mubazir dan tidak tepat sasaran,negative
Kementerian terkait melakukan evaluasi pelaksanaan program MBG di 10 daerah percontohan,neutral
Program ini nyata manfaatnya buat keluarga kami yang kurang mampu semoga terus ada,positive
"""


def render():
    inject_css()

    st.title("Prediksi Sentimen")
    st.caption("Klasifikasikan sentimen teks atau batch data CSV menggunakan model IndoBERT-CNN Dual-Path.")

    # Load model
    with st.spinner("Memuat model IndoBERT-CNN..."):
        try:
            model, tokenizer, device = load_model_and_tokenizer()
            st.success(f"Model siap · Device: {str(device).upper()}", icon="✅")
            model_loaded = True
        except FileNotFoundError as e:
            st.error(f"**Model tidak ditemukan**\n\n{e}")
            st.info("Pastikan file `indobert_cnn_dualpath_S2.pt` ada di folder `model/`")
            model_loaded = False
        except Exception as e:
            st.error(f"**Gagal memuat model:** {e}")
            model_loaded = False

    if not model_loaded:
        return

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab_text, tab_csv, tab_sample = st.tabs([
        "Input Teks",
        "Upload CSV",
        "Sample Data",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB A — INPUT TEKS MANUAL
    # ════════════════════════════════════════════════════════════════════════
    with tab_text:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        with st.container(border=True):
            teks_input = st.text_area(
                "Teks tweet",
                height=140,
                max_chars=512,
                placeholder="Ketik atau paste tweet tentang Program Makan Bergizi Gratis (MBG) di sini...",
                key="teks_input_area",
                label_visibility="collapsed",
            )

            col_btn, col_count = st.columns([1, 5])
            with col_btn:
                analyze_btn = st.button("Analisis", key="btn_analyze", type="primary", use_container_width=True)
            with col_count:
                st.markdown(
                    f"<div style='display:flex; align-items:center; height:100%;'>"
                    f"<span style='font-size:0.78rem; color:#5A5C78;'>{len(teks_input)}/512 karakter</span></div>",
                    unsafe_allow_html=True,
                )

        if analyze_btn:
            if not teks_input.strip():
                st.warning("Masukkan teks terlebih dahulu.")
            else:
                with st.spinner("Menganalisis sentimen..."):
                    result = predict_single(teks_input, model, tokenizer, device)

                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                section_header("Hasil Analisis", "")
                render_result_card(result)

                # Tampilkan perbandingan teks asli vs text_bert — section biasa, bukan collapsible
                from utils.preprocessing import preprocess as _pp
                text_bert_preview = _pp(teks_input)

                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                section_header("Detail Teks — Original vs Setelah Preprocessing", "")
                st.markdown("<div style='margin-bottom:0.5rem;'><span style='font-size:0.75rem;color:#5A5C78;text-transform:uppercase;letter-spacing:0.06em;'>Teks Original</span></div>", unsafe_allow_html=True)
                st.markdown(
                    f"""<div style="background:#141627; border:1px solid #252842;
                                  border-radius:8px; padding:0.85rem;
                                  font-size:0.88rem; color:#E8E9F3; line-height:1.6;
                                  margin-bottom:0.75rem;">
                        {html.escape(teks_input)}
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.markdown("<div style='margin-bottom:0.5rem;'><span style='font-size:0.75rem;color:#5A5C78;text-transform:uppercase;letter-spacing:0.06em;'>Setelah Preprocessing (text_bert — input ke model)</span></div>", unsafe_allow_html=True)
                st.markdown(
                    f"""<div style="background:#0D2137; border:1px solid #6C63FF40;
                                  border-radius:8px; padding:0.85rem;
                                  font-size:0.88rem; color:#A8DAFF; line-height:1.6;
                                  font-family:'JetBrains Mono', monospace;">
                        {html.escape(text_bert_preview) if text_bert_preview else "(teks terlalu pendek setelah preprocessing)"}
                    </div>""",
                    unsafe_allow_html=True,
                )

    # ════════════════════════════════════════════════════════════════════════
    # TAB B — UPLOAD CSV
    # ════════════════════════════════════════════════════════════════════════
    with tab_csv:
        _render_csv_tab(model, tokenizer, device)

    # ════════════════════════════════════════════════════════════════════════
    # TAB C — SAMPLE DATA
    # ════════════════════════════════════════════════════════════════════════
    with tab_sample:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        section_header("Sample Data MBG (10 Tweet Terkurasi)", "")

        # Load sample data dari string konstanta
        df_sample = pd.read_csv(io.StringIO(SAMPLE_DATA_CSV))
        with st.container(border=True):
            st.caption(f"{len(df_sample)} tweet sample siap digunakan.")
            st.dataframe(df_sample[["full_text"]], use_container_width=True)
            predict_sample_btn = st.button("Prediksi Sample Data", key="btn_predict_sample", type="primary")

        if predict_sample_btn:
            texts = df_sample["full_text"].fillna("").astype(str).tolist()

            with st.spinner(f"Menganalisis sentimen {len(texts)} tweet sample..."):
                results = []
                for text in texts:
                    try:
                        r = predict_single(text, model, tokenizer, device)
                    except Exception:
                        r = {"label": "neutral", "label_id": 2, "confidence": 0.0, "probs": [0.0, 0.0, 1.0]}
                    results.append(r)

            label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
            df_sample["sentimen"]    = [r["label"] for r in results]
            df_sample["sentimen_id"] = [label_id_map[r["label"]] for r in results]
            df_sample["confidence"]  = [f"{r['confidence']*100:.1f}%" for r in results]

            section_header("Hasil Prediksi Sample", "")
            st.dataframe(df_sample[["full_text", "sentimen_id", "confidence"]], use_container_width=True)

            counts = df_sample["sentimen"].value_counts()
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Pie(
                labels=["Positif", "Negatif", "Netral"],
                values=[counts.get("positive",0), counts.get("negative",0), counts.get("neutral",0)],
                hole=0.5,
                marker=dict(colors=["#10B981","#EF4444","#F59E0B"], line=dict(color="#0D0F1A",width=2)),
                textinfo="percent+label",
                textfont=dict(size=12, color="#E8E9F3"),
            )])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=250)
            st.plotly_chart(fig, use_container_width=True)


def _render_csv_tab(model, tokenizer, device):
    """
    Isi Tab "Upload CSV". Dipisah jadi fungsi tersendiri agar `return` di sini
    hanya keluar dari tab ini — bukan dari render() — sehingga error pada CSV
    tidak membuat tab lain (Sample Data) ikut kosong.
    """
    import plotly.graph_objects as go

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            """<div style="font-size:0.82rem; color:#9899B0; margin-bottom:0.75rem; line-height:1.6;">
            Upload file CSV hasil tweet-harvest atau format lain.
            Kolom yang diperlukan: kolom teks tweet (biasanya <code style="color:#6C63FF;">full_text</code>).
            Kolom lain akan tetap disertakan dalam hasil.
            </div>""",
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Pilih file CSV",
            type=["csv"],
            key="csv_uploader",
            label_visibility="collapsed",
        )

    if uploaded_file is None:
        return

    # Validasi ukuran (maks 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File terlalu besar. Maksimum 10MB.")
        return

    # Baca CSV (fallback encoding UTF-8 → Latin-1)
    try:
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="latin-1")
    except Exception as e:
        st.error(f"Gagal membaca CSV: {e}")
        return

    n_rows = len(df)
    if n_rows == 0 or len(df.columns) == 0:
        st.warning("File CSV tidak memiliki baris data untuk diproses.")
        return

    st.caption(f"{n_rows:,} baris · {len(df.columns)} kolom · {uploaded_file.size/1024:.1f} KB")

    # Pilih kolom teks
    columns = df.columns.tolist()
    default_col = "full_text" if "full_text" in columns else columns[0]
    text_col = st.selectbox(
        "Pilih kolom yang berisi teks tweet:",
        columns,
        index=columns.index(default_col),
        key="col_selector",
    )

    # Preview
    section_header("Preview Data (5 baris pertama)", "")
    st.dataframe(df[[text_col]].head(5), use_container_width=True, hide_index=False)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Batasi untuk demo agar tidak terlalu lama.
    # Slider hanya muncul jika baris > 10 (menghindari min_value > max_value).
    if n_rows <= 10:
        max_rows = n_rows
        st.caption(f"Semua {n_rows} baris akan diproses.")
    else:
        max_rows = st.slider(
            "Jumlah baris yang akan diproses:",
            min_value=10,
            max_value=min(n_rows, 500),
            value=min(n_rows, 100),
            step=10,
            key="max_rows_slider",
        )

    if not st.button(f"Prediksi {max_rows} Baris", key="btn_predict_csv", type="primary"):
        return

    df_process = df.head(max_rows).copy()
    texts = df_process[text_col].fillna("").astype(str).tolist()

    with st.spinner(f"Menganalisis sentimen {len(texts)} baris..."):
        results = []
        for text in texts:
            try:
                r = predict_single(text, model, tokenizer, device)
            except Exception:
                r = {"label": "neutral", "label_id": 2, "confidence": 0.0, "probs": [0.0, 0.0, 1.0]}
            results.append(r)

    # Tambahkan kolom hasil ke dataframe
    label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
    df_process["sentimen"]     = [r["label"] for r in results]
    df_process["sentimen_id"]  = [label_id_map[r["label"]] for r in results]
    df_process["confidence"]   = [f"{r['confidence']*100:.1f}%" for r in results]
    df_process["prob_positif"] = [f"{r['probs'][0]*100:.1f}%" for r in results]
    df_process["prob_negatif"] = [f"{r['probs'][1]*100:.1f}%" for r in results]
    df_process["prob_netral"]  = [f"{r['probs'][2]*100:.1f}%" for r in results]

    # Statistik
    section_header("Hasil Prediksi", "")

    counts  = df_process["sentimen"].value_counts()
    pos_n   = counts.get("positive", 0)
    neg_n   = counts.get("negative", 0)
    neu_n   = counts.get("neutral",  0)
    total_n = len(df_process)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Diproses", total_n)
    c2.metric("😊 Positif", pos_n, f"{pos_n/total_n*100:.1f}%", delta_color="off")
    c3.metric("😞 Negatif", neg_n, f"{neg_n/total_n*100:.1f}%", delta_color="off")
    c4.metric("😐 Netral", neu_n, f"{neu_n/total_n*100:.1f}%", delta_color="off")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Pie chart distribusi + tabel hasil
    col_chart, col_table = st.columns([1, 1.8])

    with col_chart:
        section_header("Distribusi Sentimen", "")
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Positif", "Negatif", "Netral"],
            values=[pos_n, neg_n, neu_n],
            hole=0.5,
            marker=dict(colors=["#10B981", "#EF4444", "#F59E0B"], line=dict(color="#0D0F1A", width=2)),
            textinfo="percent+label",
            textfont=dict(size=11, color="#E8E9F3"),
            hovertemplate="<b>%{label}</b><br>%{value} tweet<br>%{percent}<extra></extra>",
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=220,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_table:
        section_header("Tabel Hasil", "")
        display_cols = [text_col, "sentimen_id", "confidence", "prob_positif", "prob_negatif", "prob_netral"]
        st.dataframe(
            df_process[display_cols].rename(columns={
                text_col: "Teks",
                "sentimen_id": "Sentimen",
                "confidence": "Confidence",
                "prob_positif": "Prob Positif",
                "prob_negatif": "Prob Negatif",
                "prob_netral": "Prob Netral",
            }),
            use_container_width=True,
            height=280,
        )

    # Download button
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    csv_out = df_process.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="Download Hasil (CSV)",
        data=csv_out,
        file_name="hasil_prediksi_sentimen_mbg.csv",
        mime="text/csv",
        key="download_csv",
    )
