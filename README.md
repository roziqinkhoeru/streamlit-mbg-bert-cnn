# SentiMBG - Aplikasi Analisis Sentimen MBG

Aplikasi web berbasis Streamlit yang mengimplementasikan model IndoBERT-CNN Dual-Path untuk klasifikasi sentimen opini publik pada platform X (Twitter) mengenai **Program Makan Bergizi Gratis (MBG)**. Aplikasi ini menghasilkan klasifikasi tiga kelas: **positif**, **negatif**, dan **netral**.

## Fitur

- **Prediksi Teks Tunggal** - klasifikasi sentimen untuk satu teks yang diketik langsung
- **Prediksi Batch CSV** - klasifikasi masal dari file CSV (hingga 500 baris)
- **Prediksi Sample Data** - klasifikasi 10 tweet MBG terkurasi untuk demonstrasi cepat
- **Live Crawling** - crawling tweet langsung dari platform X berdasarkan keyword dan rentang tanggal
- **Project Showcase** - halaman informasi lengkap penelitian, arsitektur, dan performa model

## Struktur Folder

```
streamlit-mbg-bert-cnn/
├── app.py                              # Entry point + st.navigation()
├── requirements.txt
├── README.md
├── PRD.md
├── .streamlit/
│   └── config.toml
├── model/
│   ├── model_def.py                    # Definisi kelas IndoBERTCNN
│   ├── indobert_cnn_dualpath_S2.pt     # Checkpoint (unduh terpisah)
│   └── tokenizer_cache/
├── utils/
│   ├── predictor.py                    # Load model + inference
│   ├── preprocessing.py                # Pipeline preprocessing 4 tahap
│   ├── crawler.py                      # Integrasi tweet-harvest
│   └── styles.py                       # CSS global + komponen tampilan
├── pages/
│   ├── prediksi.py                     # Halaman utama prediksi
│   └── tentang.py                      # Halaman project showcase
└── assets/
    ├── sample_data.csv                 # 10 tweet MBG terkurasi
    └── kamus/                          # Kamus preprocessing custom
        ├── kamus_alay_mbg.csv
        ├── demoji_code_mbg.csv
        ├── akun_x_mbg.csv
        ├── whitelist_hashtag_mbg.csv
        └── additional_stopwords_mbg.csv
```

## Prasyarat Sistem

- Python 3.9 atau versi lebih baru
- RAM minimal 8 GB
- Ruang penyimpanan kosong 2 GB
- Akselerator opsional: NVIDIA CUDA atau Apple Silicon MPS
- Node.js v18+ (untuk fitur Live Crawling)

## Setup dan Instalasi

```bash
# 1. Clone repositori
git clone https://github.com/roziqinkhoeru/streamlit-mbg-bert-cnn.git
cd streamlit-mbg-bert-cnn

# 2. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate    # macOS / Linux
# venv\Scripts\activate     # Windows

# 3. Instalasi dependensi Python
pip install -r requirements.txt

# 4. Unduh model checkpoint
# File 'indobert_cnn_dualpath_S2.pt' tidak disertakan pada repositori.
# Unduh dari Google Drive dan letakkan pada folder model/
# Link: https://bit.ly/codembgbecnn

# 5. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis pada browser di `http://localhost:8501`.

## Fitur Live Crawling

Tab **Crawling** pada halaman prediksi mengintegrasikan library [`tweet-harvest`](https://github.com/helmisatria/tweet-harvest) berbasis Node.js dan Playwright untuk mengambil tweet secara langsung dari platform X, tanpa memerlukan API key berbayar.

**Autentikasi:** Fitur ini menggunakan `auth_token` cookie akun X yang sudah login. Cara mendapatkan token dan detail teknis crawling tersedia pada [artikel resmi tweet-harvest oleh Helmi Satria](https://helmisatria.com/blog/cara-crawl-mendapatkan-data-twitter-dengan-filter-waktu-dan-lainnya).

**Prasyarat tambahan:**

```bash
# Pastikan Node.js v18+ terpasang di sistem
node -v
```

Saat pertama kali dipanggil, `npx` akan otomatis mengunduh `tweet-harvest` beserta browser Chromium.

## Spesifikasi Model

| Atribut               | Nilai                                            |
| --------------------- | ------------------------------------------------ |
| Backbone              | `indobenchmark/indobert-base-p2`                 |
| Arsitektur            | Dual-Path [CLS] + CNN 1D Multi-Kernel            |
| Max Sequence Length   | 128 token                                        |
| Kelas Output          | Positif, Negatif, Netral                         |
| Accuracy              | 85,70%                                           |
| F1-Macro              | 0,8547                                           |
| Per-kelas F1          | Positif 0,889 \| Negatif 0,872 \| Netral 0,803  |

Detail spesifikasi teknis lengkap tersedia pada [`PRD.md`](PRD.md) dan pada halaman **Tentang** di dalam aplikasi.

## Sumber Terkait

- **Kode Penelitian Pipeline (Notebook 00-03)** - [github.com/roziqinkhoeru/mbg_bertn_cnn](https://github.com/roziqinkhoeru/mbg_bertn_cnn)
- **Repositori Data Lengkap (Google Drive)** - [bit.ly/codembgbecnn](https://bit.ly/codembgbecnn)
- **Dokumentasi Spesifikasi Produk** - [`PRD.md`](PRD.md)

---

**Departemen Informatika, Fakultas Sains dan Matematika, Universitas Diponegoro.**
