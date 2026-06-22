"""
pages/prediksi.py — Halaman Prediksi Sentimen
Tab A: Input teks manual
Tab B: Upload CSV batch prediction
Tab C: Crawling (opsional, fallback ke sample data)
"""

import streamlit as st
import pandas as pd
import io
import time
from utils.styles import inject_css, section_header, render_result_card
from utils.predictor import load_model_and_tokenizer

# Contoh tweet untuk demo
CONTOH_TWEETS = {
    "🟢 Contoh Positif": "Program makan bergizi gratis ini sangat membantu anak-anak di daerah terpencil, semoga terus berlanjut dan semakin merata ke seluruh pelosok Indonesia",
    "🔴 Contoh Negatif": "Program MBG ini pelaksanaannya kacau banget, makanan yang diberikan tidak layak dan distribusinya tidak merata sama sekali, kapan bisa diperbaiki?",
    "🟡 Contoh Netral": "Pemerintah mengumumkan bahwa program makan bergizi gratis akan diperluas ke 514 kabupaten kota mulai kuartal ketiga tahun ini",
}

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

    # Hero kecil
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h2 style="font-size:1.5rem; font-weight:700; color:#E8E9F3; margin:0 0 0.3rem 0;">
                🔍 Prediksi Sentimen
            </h2>
            <p style="font-size:0.88rem; color:#9899B0; margin:0;">
                Klasifikasikan sentimen teks atau batch data CSV menggunakan model IndoBERT-CNN Dual-Path.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load model
    with st.spinner("⏳ Memuat model IndoBERT-CNN..."):
        try:
            model, tokenizer, device = load_model_and_tokenizer()
            device_name = str(device).upper()
            st.markdown(
                f"""<div style="display:inline-flex; align-items:center; gap:0.4rem;
                              background:#10B98115; border:1px solid #10B981;
                              border-radius:100px; padding:0.25rem 0.75rem;
                              font-size:0.72rem; font-weight:600; color:#10B981;
                              margin-bottom:1rem;">
                    ✅ Model siap · Device: {device_name}
                </div>""",
                unsafe_allow_html=True,
            )
            model_loaded = True
        except FileNotFoundError as e:
            st.error(f"❌ **Model tidak ditemukan**\n\n{e}")
            st.info("Pastikan file `indobert_cnn_dualpath_S2.pt` ada di folder `model/`")
            model_loaded = False
        except Exception as e:
            st.error(f"❌ **Gagal memuat model:** {e}")
            model_loaded = False

    if not model_loaded:
        return

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab_text, tab_csv, tab_crawl = st.tabs([
        "✏️  Input Teks",
        "📄  Upload CSV",
        "🕸️  Crawling (Opsional)",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB A — INPUT TEKS MANUAL
    # ════════════════════════════════════════════════════════════════════════
    with tab_text:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        section_header("Masukkan Teks Tweet", "✏️")

        # Pilih contoh
        contoh_pilihan = st.selectbox(
            "Isi dengan contoh tweet (opsional):",
            ["— ketik sendiri —"] + list(CONTOH_TWEETS.keys()),
            key="contoh_select",
        )

        default_text = ""
        if contoh_pilihan != "— ketik sendiri —":
            default_text = CONTOH_TWEETS[contoh_pilihan]

        teks_input = st.text_area(
            "Teks tweet:",
            value=default_text,
            height=120,
            max_chars=512,
            placeholder="Ketik atau paste tweet tentang Program Makan Bergizi Gratis (MBG) di sini...",
            label_visibility="collapsed",
            key="teks_input_area",
        )

        char_count = len(teks_input)
        st.markdown(
            f"""<div style="font-size:0.72rem; color:#5A5C78; text-align:right;
                          margin-top:-0.5rem; margin-bottom:0.75rem;">
                {char_count}/512 karakter
            </div>""",
            unsafe_allow_html=True,
        )

        col_btn, col_clear = st.columns([1, 5])
        with col_btn:
            analyze_btn = st.button("🔍  Analisis", key="btn_analyze", use_container_width=True)

        if analyze_btn:
            if not teks_input.strip():
                st.warning("⚠️ Masukkan teks terlebih dahulu.")
            else:
                with st.spinner("Menganalisis sentimen..."):
                    from utils.predictor import predict_single
                    result = predict_single(teks_input, model, tokenizer, device)

                section_header("Hasil Prediksi", "📊")
                render_result_card(result, teks_input)

                # Tampilkan teks yang dianalisis
                with st.expander("📝 Teks yang dianalisis"):
                    st.markdown(
                        f"""<div style="background:#141627; border:1px solid #252842;
                                      border-radius:8px; padding:1rem;
                                      font-size:0.9rem; color:#E8E9F3; line-height:1.6;">
                            {teks_input}
                        </div>""",
                        unsafe_allow_html=True,
                    )

    # ════════════════════════════════════════════════════════════════════════
    # TAB B — UPLOAD CSV
    # ════════════════════════════════════════════════════════════════════════
    with tab_csv:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        section_header("Upload File CSV", "📄")

        st.markdown(
            """<div style="font-size:0.82rem; color:#9899B0; margin-bottom:1rem; line-height:1.6;">
            Upload file CSV hasil TwitHarvest atau format lain.
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

        if uploaded_file is not None:
            # Validasi ukuran (maks 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("❌ File terlalu besar. Maksimum 10MB.")
                return

            # Baca CSV
            try:
                try:
                    df = pd.read_csv(uploaded_file, encoding="utf-8")
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding="latin-1")
            except Exception as e:
                st.error(f"❌ Gagal membaca CSV: {e}")
                return

            st.markdown(
                f"""<div style="display:flex; gap:1.5rem; margin:0.75rem 0 1rem 0;">
                    <div style="font-size:0.8rem; color:#9899B0;">
                        📋 <b style="color:#E8E9F3;">{len(df):,}</b> baris
                    </div>
                    <div style="font-size:0.8rem; color:#9899B0;">
                        📊 <b style="color:#E8E9F3;">{len(df.columns)}</b> kolom
                    </div>
                    <div style="font-size:0.8rem; color:#9899B0;">
                        💾 <b style="color:#E8E9F3;">{uploaded_file.size/1024:.1f} KB</b>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

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
            section_header("Preview Data (5 baris pertama)", "👁️")
            st.dataframe(
                df[[text_col]].head(5),
                use_container_width=True,
                hide_index=False,
            )

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            # Batasi untuk demo agar tidak terlalu lama
            max_rows = st.slider(
                "Jumlah baris yang akan diproses:",
                min_value=10,
                max_value=min(len(df), 500),
                value=min(len(df), 100),
                step=10,
                key="max_rows_slider",
            )

            predict_btn = st.button(
                f"🚀  Prediksi {max_rows} Baris",
                key="btn_predict_csv",
                use_container_width=False,
            )

            if predict_btn:
                df_process = df.head(max_rows).copy()
                texts = df_process[text_col].fillna("").astype(str).tolist()

                # Progress bar
                progress_bar = st.progress(0)
                status_text  = st.empty()

                from utils.predictor import predict_single
                results = []
                for i, text in enumerate(texts):
                    try:
                        r = predict_single(text, model, tokenizer, device)
                    except Exception:
                        r = {"label": "neutral", "label_id": 2, "confidence": 0.0, "probs": [0.0, 0.0, 1.0]}
                    results.append(r)

                    pct = (i + 1) / len(texts)
                    progress_bar.progress(pct)
                    status_text.markdown(
                        f"<span style='font-size:0.8rem;color:#9899B0;'>Memproses baris {i+1}/{len(texts)}...</span>",
                        unsafe_allow_html=True,
                    )

                progress_bar.empty()
                status_text.empty()

                # Tambahkan kolom hasil ke dataframe
                label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
                df_process["sentimen"]       = [r["label"] for r in results]
                df_process["sentimen_id"]    = [label_id_map[r["label"]] for r in results]
                df_process["confidence"]     = [f"{r['confidence']*100:.1f}%" for r in results]
                df_process["prob_positif"]   = [f"{r['probs'][0]*100:.1f}%" for r in results]
                df_process["prob_negatif"]   = [f"{r['probs'][1]*100:.1f}%" for r in results]
                df_process["prob_netral"]    = [f"{r['probs'][2]*100:.1f}%" for r in results]

                # Statistik
                section_header("Hasil Prediksi", "✅")

                counts   = df_process["sentimen"].value_counts()
                pos_n    = counts.get("positive", 0)
                neg_n    = counts.get("negative", 0)
                neu_n    = counts.get("neutral",  0)
                total_n  = len(df_process)

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">Total Diproses</div>
                        <div class="metric-value">{total_n}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">😊 Positif</div>
                        <div class="metric-value" style="color:#10B981;">{pos_n}</div>
                        <div class="metric-sub">{pos_n/total_n*100:.1f}%</div>
                    </div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">😞 Negatif</div>
                        <div class="metric-value" style="color:#EF4444;">{neg_n}</div>
                        <div class="metric-sub">{neg_n/total_n*100:.1f}%</div>
                    </div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">😐 Netral</div>
                        <div class="metric-value" style="color:#F59E0B;">{neu_n}</div>
                        <div class="metric-sub">{neu_n/total_n*100:.1f}%</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

                # Pie chart distribusi
                import plotly.graph_objects as go
                col_chart, col_table = st.columns([1, 1.8])

                with col_chart:
                    section_header("Distribusi Sentimen", "🥧")
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=["Positif", "Negatif", "Netral"],
                        values=[pos_n, neg_n, neu_n],
                        hole=0.5,
                        marker=dict(
                            colors=["#10B981", "#EF4444", "#F59E0B"],
                            line=dict(color="#0D0F1A", width=2)
                        ),
                        textinfo="percent+label",
                        textfont=dict(size=11, color="#E8E9F3"),
                        hovertemplate="<b>%{label}</b><br>%{value} tweet<br>%{percent}<extra></extra>",
                    )])
                    fig_pie.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        showlegend=False,
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=220,
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_table:
                    section_header("Tabel Hasil", "📋")
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
                    label="⬇️  Download Hasil (CSV)",
                    data=csv_out,
                    file_name="hasil_prediksi_sentimen_mbg.csv",
                    mime="text/csv",
                    key="download_csv",
                )

    # ════════════════════════════════════════════════════════════════════════
    # TAB C — CRAWLING (OPSIONAL)
    # ════════════════════════════════════════════════════════════════════════
    with tab_crawl:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="background:#F59E0B15; border:1px solid #F59E0B40;
                        border-radius:8px; padding:1rem; margin-bottom:1rem;">
                <div style="font-size:0.8rem; color:#F59E0B; font-weight:600; margin-bottom:0.3rem;">
                    ⚠️  Fitur Opsional — Memerlukan Koneksi Internet
                </div>
                <div style="font-size:0.78rem; color:#9899B0; line-height:1.6;">
                    Fitur crawling menggunakan TwitHarvest dengan session cookie Twitter/X Anda.
                    Jika tidak tersedia, gunakan <b>Sample Data</b> untuk demo.
                    API Twitter resmi berbayar; fitur ini menggunakan metode scraping gratis
                    dengan batasan tertentu.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mode = st.radio(
            "Mode:",
            ["📦  Gunakan Sample Data (Recommended untuk Demo)", "🌐  Crawling Live (Memerlukan session cookie)"],
            key="crawl_mode",
        )

        if "Sample Data" in mode:
            section_header("Sample Data MBG (100 Tweet Terkurasi)", "📦")

            # Load sample data dari string konstanta
            df_sample = pd.read_csv(io.StringIO(SAMPLE_DATA_CSV))
            st.info(f"📊 {len(df_sample)} tweet sample siap digunakan.")
            st.dataframe(df_sample[["full_text"]].head(10), use_container_width=True)

            if st.button("🚀  Prediksi Sample Data", key="btn_predict_sample"):
                from utils.predictor import predict_single
                texts = df_sample["full_text"].fillna("").astype(str).tolist()
                results = []

                progress_bar = st.progress(0)
                for i, text in enumerate(texts):
                    try:
                        r = predict_single(text, model, tokenizer, device)
                    except Exception:
                        r = {"label": "neutral", "label_id": 2, "confidence": 0.0, "probs": [0.0, 0.0, 1.0]}
                    results.append(r)
                    progress_bar.progress((i + 1) / len(texts))

                progress_bar.empty()

                label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
                df_sample["sentimen"]    = [r["label"] for r in results]
                df_sample["sentimen_id"] = [label_id_map[r["label"]] for r in results]
                df_sample["confidence"]  = [f"{r['confidence']*100:.1f}%" for r in results]

                section_header("Hasil Prediksi Sample", "✅")
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

        else:  # Live crawling
            section_header("Crawling Live dari Twitter/X", "🌐")

            st.markdown(
                """<div style="font-size:0.8rem; color:#9899B0; margin-bottom:1rem; line-height:1.6;">
                Fitur ini menggunakan TwitHarvest (open-source). Anda perlu menyediakan
                <b style="color:#6C63FF;">session cookie (auth_token)</b> dari akun Twitter/X yang sudah login.
                </div>""",
                unsafe_allow_html=True,
            )

            keyword = st.text_input(
                "Keyword pencarian:",
                value="makan bergizi gratis",
                key="crawl_keyword",
            )
            auth_token = st.text_input(
                "auth_token (dari cookie Twitter/X):",
                type="password",
                key="crawl_auth",
                placeholder="Paste auth_token dari developer tools browser Anda",
            )
            n_tweets = st.slider("Jumlah tweet:", 50, 500, 100, 50, key="crawl_n")

            if st.button("🕸️  Mulai Crawling", key="btn_crawl"):
                if not auth_token:
                    st.warning("⚠️ auth_token diperlukan untuk crawling.")
                else:
                    try:
                        import subprocess, json, tempfile, sys

                        st.info("⏳ Melakukan crawling... (bisa memakan waktu 30–60 detik)")
                        with st.spinner("Crawling Twitter/X..."):
                            # Coba gunakan TwitHarvest jika terinstall
                            result = subprocess.run(
                                [sys.executable, "-m", "twitharvest",
                                 "--query", keyword,
                                 "--limit", str(n_tweets),
                                 "--auth_token", auth_token,
                                 "--output", "json"],
                                capture_output=True, text=True, timeout=120,
                            )
                            if result.returncode != 0:
                                raise Exception(f"TwitHarvest error: {result.stderr[:200]}")
                            data = json.loads(result.stdout)
                            df_crawl = pd.DataFrame(data)

                        st.success(f"✅ Berhasil crawl {len(df_crawl)} tweet.")
                        st.dataframe(df_crawl[["full_text"]].head(5), use_container_width=True)

                    except FileNotFoundError:
                        st.error("❌ TwitHarvest tidak terinstall. Jalankan: `pip install twitharvest`")
                    except Exception as e:
                        st.error(f"❌ Crawling gagal: {e}")
                        st.info("💡 Gunakan mode **Sample Data** untuk melanjutkan demo.")
