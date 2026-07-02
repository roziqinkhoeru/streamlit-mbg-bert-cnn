# PRD — MBG Sentiment Analysis Demo App

**Product Requirements Document & System Review**
Analisis Sentimen Opini Publik Program Makan Bergizi Gratis (MBG) menggunakan IndoBERT-CNN Dual-Path

| | |
|---|---|
| **Versi Dokumen** | 1.0 |
| **Tanggal** | 2026-06-24 |
| **Status** | Selesai (artefak demo sidang skripsi) |
| **Penulis Sistem** | Khoeru Roziqin — Informatika S1 |
| **Jenis Produk** | Aplikasi web demo (research artifact) untuk sidang skripsi & dokumentasi HKI |
| **Entry point** | `streamlit run app.py` |

---

## 1. Ringkasan Eksekutif

Aplikasi web berbasis **Streamlit** yang mendemonstrasikan model *deep learning* hasil penelitian skripsi:
klasifikasi sentimen tiga kelas (**Positif / Negatif / Netral**) terhadap opini publik berbahasa Indonesia
di platform X (Twitter) mengenai program pemerintah **Makan Bergizi Gratis (MBG)**.

Inti sistem adalah model hibrida **IndoBERT-CNN Dual-Path** — menggabungkan representasi konteks global
(`[CLS]` dari IndoBERT) dengan pola n-gram lokal (CNN 1D multi-kernel). Aplikasi membungkus model ini dalam
antarmuka interaktif dua halaman: **Home** (prediksi) dan **Tentang** (project showcase).

Aplikasi berfungsi sebagai **bukti fungsional** dan **alat presentasi** untuk sidang skripsi — bukan produk
komersial. Fokusnya adalah reproduktibilitas hasil penelitian (menghindari *train-serve skew*), kejelasan
visual, dan kemudahan demonstrasi langsung.

---

## 2. Latar Belakang & Tujuan

### 2.1 Masalah

Program MBG memicu volume percakapan publik yang besar di media sosial. Menilai sentimen publik secara manual
tidak *scalable*. Diperlukan sistem klasifikasi otomatis yang:
- akurat untuk teks informal berbahasa Indonesia (slang, singkatan, emoji),
- mampu menangkap konteks global sekaligus pola frasa lokal,
- dapat didemonstrasikan secara langsung dan transparan.

### 2.2 Tujuan Produk

| # | Tujuan | Ukuran Keberhasilan |
|---|--------|---------------------|
| G1 | Mendemonstrasikan model hasil penelitian secara *live* | Prediksi teks tunggal < 1 detik setelah warm-up |
| G2 | Menjamin hasil identik dengan pipeline training | Preprocessing di serving = NB02 (no train-serve skew) |
| G3 | Menyajikan hasil penelitian secara profesional | Halaman Tentang sebagai project showcase lengkap |
| G4 | Mendukung input fleksibel | Input manual, batch CSV, dan sample data |
| G5 | Reprodusibel di mesin lokal | Setup via `requirements.txt` + checkpoint manual |

### 2.3 Non-Tujuan (Out of Scope)

- **Crawling data live** — sempat dieksplorasi (tweet-harvest / tweety-ns), lalu **dihapus** karena tidak
  andal di lingkungan free-tier dan menambah dependency non-Python (Node.js + Playwright). Pengumpulan data
  penelitian dilakukan terpisah via `Fix Crawling MBG.ipynb` (Google Colab).
- Training / fine-tuning model dari dalam aplikasi.
- Autentikasi pengguna, multi-tenant, atau persistensi database.
- Deployment publik berskala (aplikasi ditargetkan untuk demo lokal).

---

## 3. Pengguna & Persona

| Persona | Kebutuhan | Cara Pakai |
|---------|-----------|------------|
| **Penguji sidang** | Verifikasi klaim penelitian secara langsung | Ketik contoh tweet → lihat prediksi + confidence |
| **Peneliti (penulis)** | Presentasi metodologi & hasil | Halaman Tentang + demo interaktif |
| **Reviewer teknis / dosen** | Menilai arsitektur & metrik | Confusion matrix, F1 per kelas, arsitektur model |
| **Pengguna umum (opsional)** | Coba klasifikasi teks sendiri | Batch CSV atau sample data |

---

## 4. Arsitektur Sistem

### 4.1 Diagram Alur Tingkat Tinggi

```
                    app.py  (st.navigation / st.Page)
                       │
        ┌──────────────┴───────────────┐
   pages/prediksi.py            pages/tentang.py
   (Home — 3 tab)               (Project showcase)
        │
        │ predict_single()
        ▼
   utils/predictor.py ──► utils/preprocessing.py  (4-step pipeline, kamus/*.csv)
        │
        ▼
   model/model_def.py  (IndoBERTCNN)  ◄── model/indobert_cnn_dualpath_S2.pt (checkpoint)
        │
   utils/styles.py  (CSS global, injected per halaman)
```

### 4.2 Modul & Tanggung Jawab

| Modul | Peran | Catatan Arsitektural |
|-------|-------|----------------------|
| `app.py` | Entry point, routing, sidebar | Wajib pakai `st.navigation()` — mencegah Streamlit auto-generate nav ganda dari folder `pages/` |
| `pages/prediksi.py` | Halaman Home: 3 tab prediksi | Tab: Input Teks, Upload CSV, Sample Data |
| `pages/tentang.py` | Project showcase (metrik, arsitektur, dataset, metodologi, referensi) | Gabungan dari halaman Dashboard + Tentang lama |
| `utils/predictor.py` | Load model + inference | `@st.cache_resource`, device auto-select, warm-up |
| `utils/preprocessing.py` | Pipeline 4-langkah (identik NB02) | Kamus slang/emoji/akun; Nasal auto-download & cache |
| `model/model_def.py` | Definisi `IndoBERTCNN` | Harus identik dengan notebook training |
| `utils/styles.py` | CSS global dark theme + `render_result_card()` | HTML flush-left untuk hindari bug parser markdown |
| `.streamlit/config.toml` | Tema & konfigurasi runtime | `toolbarMode=minimal`, tema dark |

### 4.3 Keputusan Arsitektural Kunci (Load-Bearing)

1. **`st.navigation()` bukan folder `pages/` auto-discovery** — Streamlit otomatis memindai folder bernama
   `pages/` dan membuat sidebar navigasi kedua yang bertabrakan. Memanggil `st.navigation()` eksplisit
   menonaktifkan perilaku ini. Modul halaman meng-*expose* fungsi `render()` tanpa argumen.
2. **Checkpoint = wrapper dict**, bukan flat state_dict. Struktur:
   `{model_state_dict, architecture, lr_config, cnn_config, fixed_config}`. Selalu ekstrak `model_state_dict`.
3. **`weights_only=False` disengaja** — checkpoint berisi objek numpy non-tensor (`numpy.dtype`, numpy scalar)
   yang ditolak default PyTorch ≥2.6. Aman karena checkpoint adalah artefak milik sendiri (*trusted*).
4. **Preprocessing wajib sebelum tokenisasi** — model dilatih pada kolom `text_bert`, bukan `full_text`.
   Melewati preprocessing → *train-serve skew*.
5. **HTML flush-left di `st.markdown(unsafe_allow_html=True)`** — HTML berindentasi bisa disalahartikan parser
   markdown sebagai *code block*, menyebabkan tag literal (`</div>`) ter-render sebagai teks.

---

## 5. Spesifikasi Model & Data

### 5.1 Arsitektur Model — IndoBERTCNN Dual-Path

```
Input Tweet → IndoBERT (indobert-base-p2) → last_hidden_state [batch, 128, 768]
                                  │
              ┌───────────────────┴────────────────────┐
       Path 1: [CLS] token                   Path 2: CNN 1D multi-kernel
       (konteks global)                      (pola n-gram lokal, k=[1,2,3])
       Dropout(0.1)                          Conv1d ×3 → ELU → GlobalMaxPool
       [batch, 768]                          [batch, 256×3 = 768]
              └───────────── Concatenate [batch, 1.152] ─────────────┘
                                  │
              Dropout(0.5) → Dense(256, ELU) → Dropout(0.5) → Dense(3) → Softmax
                                  │
                    [Positif | Negatif | Netral]
```

Path CNN **melengkapi** `[CLS]`, bukan menggantikan.

### 5.2 Hyperparameter (harus identik dengan training)

| Parameter | Nilai | Parameter | Nilai |
|-----------|-------|-----------|-------|
| Backbone | `indobenchmark/indobert-base-p2` | Dropout (head) | 0.5 |
| N-gram (kernel CNN) | [1, 2, 3] | CLS Dropout | 0.1 |
| Filter size | 256 | Dense size | 256 (ELU) |
| Activation | ELU | Max length | 128 token |
| LR BERT / CNN | 1e-5 / 1e-4 | Batch size | 32 |
| Weight decay | 0.01 | Validasi | 5-Fold Stratified CV |

### 5.3 Label Mapping (kritis)

```python
ID2LABEL = {0: "positive", 1: "negative", 2: "neutral"}
```
⚠️ Urutan **non-standar** (positive=0). Harus identik dengan urutan saat training. Divalidasi empiris:
kalimat positif→positive, negatif→negative, netral→neutral.

### 5.4 Dataset

| Atribut | Nilai |
|---------|-------|
| Sumber | Platform X (Twitter) |
| Tools scraping | tweet-harvest (Node.js/Playwright) — *di luar aplikasi* |
| Kata kunci | "mbg", "makan bergizi gratis" |
| Periode | Januari 2025 – Januari 2026 |
| Total raw | 172.009 tweet |
| Total berlabel | 6.642 tweet (manual annotation) |
| Distribusi | Positif 2.625 (39.5%) · Negatif 2.085 (31.4%) · Netral 1.932 (29.1%) |
| Split | Train/Val 5.313 (80%) · Test 1.329 (20%, fixed) |
| Imbalance handling | Random Undersampling (kondisi S2 — terpilih vs S1 Class Weighting) |

### 5.5 Performa Model (Test Set, 1.329 tweet)

| Metrik | Nilai | | F1 per Kelas | Nilai |
|--------|-------|---|--------------|-------|
| **F1-Macro** | **0.8547** | | Positif | 0.8891 |
| **Accuracy** | **85.70%** | | Negatif | 0.8717 |
| Precision (macro) | 0.8551 | | Netral | 0.8034 |
| Recall (macro) | 0.8585 | | | |

### 5.6 Pipeline Preprocessing (4 langkah, identik NB02)

1. **Case folding & HTML unescape** — lowercase, decode entitas HTML.
2. **Cleaning** — hapus URL/mention/hashtag non-whitelist, emoji→frasa, normalisasi mata uang/tanggal/angka,
   emotikon ASCII→kata, repetisi huruf.
3. **Tokenization** — whitespace split (helper untuk langkah 4).
4. **Normalization** — normalisasi slang (kamus Nasal + custom), negasi (`gak`/`nggak`→`tidak`), dedup frasa.
   Output: `text_bert`.

Kamus (`assets/kamus/*.csv`): degradasi anggun bila file hilang (dict kosong, no crash), kecuali kamus Nasal
yang **auto-download** & cache di `colloquial-indonesian-lexicon.csv`. `_load_all_dicts()` di-cache.

---

## 6. Requirement Fungsional

### FR-1 — Prediksi Teks Tunggal (Tab "Input Teks")
- Input `text_area` maks 512 karakter + penghitung karakter.
- Tombol "Analisis" (primary) → `predict_single()` dengan spinner "Menganalisis sentimen...".
- Output **result card**: Kategori Sentimen (berwarna + emoji), Confidence Score, dan 3 progress bar
  probabilitas per kelas.
- Section "Detail Teks" (bukan collapsible): perbandingan teks Original vs `text_bert` setelah preprocessing.

### FR-2 — Prediksi Batch CSV (Tab "Upload CSV")
- Upload CSV (maks 10MB), fallback encoding UTF-8 → Latin-1.
- Auto-deteksi kolom `full_text` (fallback kolom pertama), preview 5 baris.
- Slider jumlah baris (10–500, step 10, default 100).
- Prediksi dengan spinner batch → metrik ringkas (4 kolom), pie chart distribusi, tabel hasil + probabilitas,
  dan tombol download CSV hasil (`utf-8-sig`).

### FR-3 — Prediksi Sample Data (Tab "Sample Data")
- 10 tweet MBG terkurasi (positif/negatif/netral) sebagai demo cepat tanpa upload.
- Prediksi dengan spinner → tabel hasil + pie chart distribusi.

### FR-4 — Project Showcase (Halaman "Tentang")
- Hero + highlight strip (Accuracy, F1-Macro, ukuran dataset, jumlah kelas).
- Profil peneliti + judul skripsi + abstrak.
- Metrik performa, F1 per kelas, distribusi dataset (donut), confusion matrix (heatmap).
- Diagram arsitektur, tabel hyperparameter, hasil K-Fold (S1 vs S2).
- Informasi dataset, langkah metodologi, referensi utama, tech stack.

### FR-5 — Loading & Error State
- Model di-load sekali per sesi (`@st.cache_resource`) dengan spinner + badge status device.
- Error `FileNotFoundError` → pesan setup checkpoint; error lain → pesan gagal load.
- Semua prediksi (tunggal & batch) memakai `st.spinner` dengan keterangan kontekstual.

---

## 7. Requirement Non-Fungsional

| Kategori | Requirement / Implementasi |
|----------|----------------------------|
| **Performa (cold start)** | Tokenizer di-cache lokal (`model/tokenizer_cache/`), warm-up forward pass, `@st.cache_resource` |
| **Performa (inference)** | Device auto-select: **MPS > CUDA > CPU** |
| **Kompatibilitas** | PyTorch ≥2.0, transformers ≥4.40, Python 3.9+ (diuji 3.9) |
| **Reprodusibilitas** | Preprocessing identik training; config model hardcoded + tersimpan di checkpoint |
| **Ketahanan (resilience)** | Kamus hilang → degradasi anggun; prediksi batch gagal per-item → fallback neutral |
| **UX / Visual** | Dark theme konsisten, native Streamlit primitives (`st.container(border=True)`, `st.metric`), ikon Material tetap ter-render |
| **Batasan input** | CSV maks 10MB / 500 baris; teks maks 512 karakter |

---

## 8. Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Frontend / App | Streamlit ≥1.35 (native multipage `st.navigation`) |
| Model / Inference | PyTorch ≥2.0, HuggingFace Transformers ≥4.40, IndoBERT (`indobert-base-p2`) |
| Data | pandas ≥2.0, numpy ≥1.24 |
| Visualisasi | Plotly ≥5.18 |
| Tokenisasi | sentencepiece, protobuf |
| Utilitas | requests (auto-download kamus Nasal) |

---

## 9. Temuan Deep Review

### 9.1 Kualitas & Kebenaran (Correctness)

| # | Temuan | Severity | Rekomendasi |
|---|--------|----------|-------------|
| C1 | Label mapping urutan non-standar (`positive=0`) | ⚠️ Info | Sudah divalidasi empiris & konsisten dipakai. Pertahankan; jangan ubah tanpa cek notebook training. |
| C2 | `weights_only=False` saat load checkpoint | ⚠️ Info | Aman untuk artefak sendiri. Jika suatu saat deploy publik, jangan load checkpoint dari sumber tak terpercaya. |
| C3 | Teks pengguna diinterpolasi ke `unsafe_allow_html` tanpa escaping (section "Detail Teks Original") | 🟡 Low | Risiko rendah untuk demo lokal single-user. Bila deploy publik: bungkus `teks_input` dengan `html.escape()` (mitigasi reflected-HTML/XSS). |
| C4 | Fallback preprocessing (<2 kata → teks mentah) melewati proteksi train-serve skew | 🟡 Low | Dampak minor pada input sangat pendek; terima sebagai *tradeoff* atau beri catatan pada UI. |

### 9.2 Kebersihan Kode (Cleanliness / Dead Code)

| # | Temuan | Rekomendasi |
|---|--------|-------------|
| D1 | `predict_batch()` di `predictor.py` tidak lagi dipakai (tab batch pakai loop inline `predict_single`) | Hapus, atau refactor tab batch untuk memakainya kembali (DRY) |
| D2 | `import time` di `prediksi.py` tidak terpakai | Hapus |
| D3 | `additional_stopwords_mbg.csv` ada tapi tidak di-load `preprocessing.py` | Wajar (pipeline BERT tanpa stopword removal). Hapus file jika benar-benar tak dipakai, atau dokumentasikan. |
| D4 | Konstanta `LABEL2ID` / `LABEL_NAMES` diekspor tapi minim pemakaian | Simpan bila untuk referensi; opsional dibersihkan |

### 9.3 Efisiensi & Skalabilitas

| # | Temuan | Rekomendasi |
|---|--------|-------------|
| E1 | Prediksi batch bersifat **sekuensial** (1 teks per forward pass), bukan *batched* melalui model | Untuk 500 baris bisa lambat. Peluang optimasi: tokenisasi & inferensi dalam *mini-batch* (mis. 32) untuk percepatan signifikan di GPU/MPS. |
| E2 | Preprocessing memuat kamus besar (Nasal ~3MB) sekali via cache | Sudah optimal (`@st.cache_resource`). |

### 9.4 Ketahanan & Deployment

| # | Temuan | Rekomendasi |
|---|--------|-------------|
| R1 | Tidak ada test suite / linter | Untuk skripsi dapat diterima. Bila dilanjutkan: tambah smoke test untuk `predict_single` (3 kalimat label diketahui) & validasi pipeline preprocessing. |
| R2 | Checkpoint 481MB git-ignored, wajib ditaruh manual | Terdokumentasi di README/CLAUDE.md. Pertimbangkan Git LFS / rilis terpisah bila perlu distribusi. |
| R3 | Aplikasi ditargetkan lokal (bukan cloud) | Sesuai tujuan. Untuk Streamlit Community Cloud: perlu strategi hosting checkpoint & pastikan MPS/GPU tidak diasumsikan. |

---

## 10. Struktur Proyek

```
streamlit-mbg-bert-cnn/
├── app.py                     # Entry point + st.navigation routing
├── requirements.txt
├── CLAUDE.md                  # Panduan arsitektur untuk agent/dev
├── README.md                  # Setup & run
├── PRD.md                     # Dokumen ini
├── .streamlit/
│   └── config.toml            # Tema dark + toolbarMode minimal
├── model/
│   ├── model_def.py           # class IndoBERTCNN
│   ├── indobert_cnn_dualpath_S2.pt   # checkpoint (git-ignored, manual)
│   └── tokenizer_cache/       # cache tokenizer (di-commit)
├── utils/
│   ├── predictor.py           # load + inference (cache, warm-up, device)
│   ├── preprocessing.py       # pipeline 4-langkah (identik NB02)
│   └── styles.py              # CSS global + render_result_card()
├── pages/
│   ├── prediksi.py            # Home (Input Teks / Upload CSV / Sample Data)
│   └── tentang.py             # Project showcase
└── assets/kamus/              # kamus slang/emoji/akun/hashtag/lexicon
```

---

## 11. Roadmap / Rekomendasi Lanjutan (Opsional)

| Prioritas | Item | Sumber |
|-----------|------|--------|
| Tinggi | Batched inference untuk tab CSV (percepatan 500 baris) | E1 |
| Sedang | Hapus dead code (`predict_batch`, `import time`) | D1, D2 |
| Sedang | Escape HTML pada input pengguna bila akan deploy publik | C3 |
| Rendah | Smoke test minimal untuk regresi prediksi | R1 |
| Rendah | Git LFS / rilis untuk checkpoint | R2 |

---

## 12. Kesimpulan

Sistem telah **memenuhi seluruh tujuan produk (G1–G5)**: model penelitian dapat didemonstrasikan secara live,
hasil terjaga identik dengan pipeline training (tanpa train-serve skew), disajikan dalam antarmuka dua halaman
yang profesional, mendukung input manual/CSV/sample, dan reprodusibel di mesin lokal. Kualitas kode baik untuk
konteks artefak skripsi; temuan review bersifat *minor* (dead code, potensi optimasi batch, catatan keamanan
untuk skenario deploy publik) dan tidak menghalangi fungsi inti. Aplikasi **siap dipakai untuk demonstrasi
sidang**.
