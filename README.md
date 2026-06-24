# MBG Sentiment Analysis — Demo App

Aplikasi demo analisis sentimen Program Makan Bergizi Gratis (MBG)
menggunakan model IndoBERT-CNN Dual-Path.

## Struktur Folder

```
mbg-sentiment-demo/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── assets/
│   └── kamus/                        ← kamus preprocessing (slang, emoji, dll.)
├── model/
│   ├── model_def.py
│   └── indobert_cnn_dualpath_S2.pt   ← LETAKKAN MODEL DI SINI
├── utils/
│   ├── predictor.py
│   ├── preprocessing.py
│   ├── crawler.py                    ← crawling tweet via tweet-harvest (Node.js)
│   └── styles.py
└── pages/
    ├── prediksi.py   (Home — prediksi sentimen)
    └── tentang.py    (project showcase + about)
```

## Setup & Jalankan

```bash
# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Letakkan model di folder model/
# Salin indobert_cnn_dualpath_S2.pt ke folder model/

# 4. Jalankan
streamlit run app.py
```

### Fitur Crawling (opsional)

Tab "Crawling (Opsional)" di halaman Home memakai
[tweet-harvest](https://github.com/helmisatria/tweet-harvest) (Node.js +
Playwright, tanpa API key berbayar) untuk mengambil tweet langsung dari
Twitter/X menggunakan `auth_token` (cookie) akun yang sudah login. Ini
adalah library yang sama dengan yang dipakai di `Fix Crawling MBG.ipynb`
untuk mengumpulkan dataset penelitian.

Prasyarat tambahan (di luar `requirements.txt`, karena bukan package Python):

```bash
# Node.js v18+ harus terpasang di sistem
node -v   # cek dulu, install dari https://nodejs.org jika belum ada
```

`npx` akan otomatis mengunduh `tweet-harvest` + browser Chromium (via
Playwright) saat pertama kali dipanggil. Jika muncul error semacam
`Target page, context or browser has been closed` atau Chromium crash,
cache browser Playwright kemungkinan corrupt — perbaiki dengan:

```bash
npx -y playwright@1.41.1 install chromium --force
```

Catatan: fitur ini butuh akses shell untuk menjalankan Node.js & browser
headless, jadi hanya berjalan di mesin/server yang Anda kendalikan sendiri
(laptop, VM, dsb.) — tidak akan berjalan di platform Python-only tanpa
Node.js seperti Streamlit Community Cloud default. Jika tidak tersedia,
gunakan mode **Sample Data** di tab yang sama.

## Model

- File: `model/indobert_cnn_dualpath_S2.pt`
- Backbone: `indobenchmark/indobert-base-p2`
- Arsitektur: Dual-Path [CLS] + CNN 1D
- F1-Macro: 0.8547 | Accuracy: 85.70%
