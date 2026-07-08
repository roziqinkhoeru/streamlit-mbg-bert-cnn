# Product Requirements Document (PRD)
## SentiMBG - Aplikasi Analisis Sentimen Program Makan Bergizi Gratis

| Field                | Value                                        |
| -------------------- | -------------------------------------------- |
| **Nama Produk**      | SentiMBG                                     |
| **Jenis**            | Aplikasi Web Analisis Sentimen               |
| **Versi Dokumen**    | 1.0                                          |
| **Status**           | Released                                     |
| **Framework**        | Streamlit                                    |
| **Bahasa Antarmuka** | Bahasa Indonesia                             |
| **Repositori**       | github.com/roziqinkhoeru/streamlit-mbg-bert-cnn |

---

## 1. Ringkasan Eksekutif

SentiMBG adalah aplikasi web berbasis framework **Streamlit** yang menyediakan analisis sentimen otomatis terhadap opini publik pada platform X (Twitter) mengenai **Program Makan Bergizi Gratis (MBG)**. Aplikasi ini mengimplementasikan model deep learning **IndoBERT-CNN Dual-Path** yang mengklasifikasikan teks berbahasa Indonesia ke dalam tiga kelas sentimen: **positif**, **negatif**, dan **netral**.

Aplikasi dirancang untuk mendemonstrasikan hasil penelitian dalam antarmuka interaktif yang dapat digunakan oleh peneliti, penguji akademik, dan pengguna umum untuk mengeksplorasi kapabilitas model pada berbagai skenario input, mulai dari teks tunggal, batch dataset, hingga data live dari platform X.

---

## 2. Latar Belakang dan Tujuan

### 2.1 Latar Belakang

Program Makan Bergizi Gratis (MBG) merupakan program strategis nasional yang menarik atensi publik secara luas di platform media sosial. Analisis sentimen otomatis terhadap opini publik memberikan wawasan cepat mengenai persepsi masyarakat, respons terhadap implementasi program, dan area yang menjadi fokus diskusi.

Model hasil penelitian tesis berjudul *"Analisis Sentimen Opini Publik di Platform Media Sosial X Mengenai Program Makan Bergizi Gratis Menggunakan BERT-CNN"* perlu disajikan dalam bentuk aplikasi web yang dapat diakses secara interaktif untuk keperluan demonstrasi, verifikasi, dan pemanfaatan lebih lanjut.

### 2.2 Tujuan Produk

- Menyajikan model IndoBERT-CNN Dual-Path hasil penelitian dalam bentuk aplikasi web interaktif.
- Menyediakan multi-mode input agar pengguna dapat mengeksplorasi model pada berbagai skenario (teks tunggal, batch CSV, sample terkurasi, dan data live crawling).
- Memberikan project showcase yang menampilkan spesifikasi teknis, metodologi penelitian, dan performa model secara transparan.
- Menjadi referensi implementasi model NLP berbahasa Indonesia untuk domain analisis sentimen media sosial.

### 2.3 Ruang Lingkup Produk

SentiMBG mencakup ruang lingkup sebagai berikut:

- Klasifikasi sentimen tiga kelas untuk teks berbahasa Indonesia.
- Domain optimal: konten media sosial (tweet) dengan gaya informal dan konteks Program Makan Bergizi Gratis.
- Deployment: aplikasi berjalan pada lingkungan lokal pengguna dengan dukungan akselerator opsional (MPS/CUDA).

---

## 3. Target Pengguna

| Persona                    | Kebutuhan Utama                                                       | Mode Input Utama                    |
| -------------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| **Peneliti / Pengembang**  | Verifikasi model, eksplorasi arsitektur, referensi implementasi       | Batch CSV, Sample, Live Crawling    |
| **Penguji Akademik**       | Demonstrasi model, verifikasi klaim penelitian, project showcase      | Sample, Teks Tunggal                |
| **Analis Data / Praktisi** | Analisis batch dataset opini, ekstraksi insight                       | Batch CSV, Live Crawling            |
| **Pengguna Umum**          | Eksplorasi teknologi analisis sentimen berbahasa Indonesia            | Teks Tunggal, Sample                |

---

## 4. Ruang Lingkup Fitur

### 4.1 Peta Fitur

SentiMBG terdiri dari dua halaman utama dengan fitur berikut:

**Halaman Prediksi Sentimen (Home)**
1. Prediksi Teks Tunggal (Tab Input Teks)
2. Prediksi Batch CSV (Tab Upload CSV)
3. Prediksi Sample Data (Tab Sample Data)
4. Live Crawling Data (Tab Crawling Opsional)

**Halaman Tentang (Project Showcase)**
5. Informasi Penelitian dan Metodologi
6. Visualisasi Performa dan Arsitektur Model

### 4.2 Requirements Fungsional

#### FR-1: Prediksi Teks Tunggal

**Deskripsi:** Pengguna dapat memasukkan satu teks bebas untuk memperoleh klasifikasi sentimen secara instan.

**Detail:**
- Input berupa text area dengan batas 512 karakter.
- Output menampilkan kategori sentimen, confidence score, dan probabilitas per kelas dalam bentuk result card.
- Progress bar visual untuk setiap kelas mempermudah interpretasi hasil.

**Kriteria Sukses:** Prediksi ditampilkan dalam waktu kurang dari 3 detik pada mode CPU dan kurang dari 1 detik pada mode akselerator (MPS/CUDA).

---

#### FR-2: Prediksi Batch CSV

**Deskripsi:** Pengguna dapat mengunggah file CSV berisi kumpulan teks untuk memperoleh prediksi sentimen secara masal.

**Detail:**
- Format file: CSV dengan ukuran maksimal 10 MB.
- Sistem melakukan deteksi otomatis kolom teks berdasarkan heuristik nama kolom (misal `text`, `tweet`, `full_text`).
- Preview 5 baris pertama ditampilkan untuk verifikasi sebelum inference.
- Pengguna dapat memilih jumlah baris yang diprediksi via slider (rentang 10–500 baris).
- Output meliputi tabel hasil, chart distribusi kelas, dan tombol unduh CSV hasil prediksi.

**Kriteria Sukses:** Batch 500 baris terproses dalam waktu kurang dari 60 detik pada mode akselerator.

---

#### FR-3: Prediksi Sample Data

**Deskripsi:** Pengguna dapat mendemonstrasikan model dengan cepat menggunakan sample tweet terkurasi tanpa perlu menyediakan data sendiri.

**Detail:**
- Sepuluh tweet MBG terkurasi disediakan dalam `assets/sample_data.csv`.
- Prediksi seluruh sample dijalankan dengan satu klik tombol.
- Output berupa tabel hasil klasifikasi lengkap dengan chart distribusi kelas.

**Kriteria Sukses:** Prediksi seluruh sample selesai dalam waktu kurang dari 5 detik pada mode akselerator.

---

#### FR-4: Live Crawling Data

**Deskripsi:** Pengguna dapat melakukan crawling tweet secara langsung dari platform X untuk dianalisis sentimennya, tanpa memerlukan API key berbayar.

**Detail:**
- Integrasi dengan library [`tweet-harvest`](https://github.com/helmisatria/tweet-harvest) v2.7.1 berbasis Node.js dan Playwright.
- Autentikasi menggunakan `auth_token` cookie X yang disediakan pengguna.
- Parameter crawling: keyword, rentang tanggal (`since`/`until`), bahasa (`lang:id`), dan limit tweet.
- Hasil crawling otomatis dialirkan ke pipeline prediksi setelah selesai.
- Kolom teks (`full_text`) langsung digunakan sebagai input untuk klasifikasi sentimen.

**Kriteria Sukses:** Crawling 100 tweet terselesaikan dan hasil prediksi ditampilkan dalam waktu kurang dari 3 menit.

---

#### FR-5: Project Showcase (Halaman Tentang)

**Deskripsi:** Halaman terintegrasi yang menampilkan informasi lengkap penelitian, arsitektur, dan performa model.

**Detail:**
- Highlight strip metrik utama: Accuracy, F1-Macro, ukuran dataset, jumlah kelas.
- Profil peneliti, judul skripsi, dan abstrak penelitian.
- Metrik performa model beserta F1 per kelas.
- Visualisasi distribusi dataset dan confusion matrix.
- Diagram arsitektur model beserta tabel hyperparameter.
- Ringkasan hasil validasi K-Fold Cross-Validation.
- Informasi dataset, langkah metodologi, referensi utama, dan tech stack.

**Kriteria Sukses:** Konten menampilkan seluruh spesifikasi teknis dan hasil penelitian dalam satu halaman terstruktur.

---

#### FR-6: State Feedback UI

**Deskripsi:** Aplikasi memberikan umpan balik visual yang jelas selama proses eksekusi berlangsung.

**Detail:**
- Loading state ditampilkan saat model dimuat atau inference dijalankan.
- Progress indicator untuk operasi batch prediction dan crawling.
- Pesan status informatif untuk setiap tahap proses.
- Konfirmasi visual saat operasi selesai (result card, chart, download button).

**Kriteria Sukses:** Setiap operasi asynchronous memiliki indikator visual yang jelas dari mulai hingga selesai.

---

## 5. Alur Pengguna

### 5.1 Alur Prediksi Teks Tunggal

```
Pengguna membuka aplikasi
   → Pilih tab "Input Teks"
   → Masukkan teks pada text area
   → Klik "Analisis"
   → Sistem menjalankan preprocessing → tokenization → inference
   → Result card ditampilkan (kategori, confidence, probabilitas)
```

### 5.2 Alur Prediksi Batch CSV

```
Pengguna membuka aplikasi
   → Pilih tab "Upload CSV"
   → Unggah file CSV (maksimal 10 MB)
   → Sistem mendeteksi kolom teks dan menampilkan preview
   → Pengguna memilih jumlah baris via slider
   → Klik "Analisis Batch"
   → Sistem menjalankan preprocessing dan inference batch
   → Tabel hasil + chart distribusi ditampilkan
   → Pengguna dapat mengunduh CSV hasil prediksi
```

### 5.3 Alur Prediksi Sample Data

```
Pengguna membuka aplikasi
   → Pilih tab "Sample Data"
   → Klik "Analisis Sample"
   → Sistem menjalankan prediksi untuk 10 tweet sample
   → Tabel hasil + chart distribusi ditampilkan
```

### 5.4 Alur Live Crawling

```
Pengguna membuka aplikasi
   → Pilih tab "Crawling"
   → Masukkan auth_token X + parameter crawling (keyword, tanggal, limit)
   → Klik "Mulai Crawling"
   → Sistem menjalankan tweet-harvest melalui Node.js
   → Tweet hasil crawling ditampilkan
   → Klik "Analisis Hasil Crawling"
   → Sistem menjalankan preprocessing dan inference batch
   → Tabel hasil + chart distribusi ditampilkan
```

### 5.5 Alur Eksplorasi Project Showcase

```
Pengguna membuka aplikasi
   → Pilih menu "Tentang" pada sidebar
   → Halaman project showcase ditampilkan
   → Pengguna dapat menelusuri informasi penelitian, arsitektur, metrik, dataset, dan metodologi
```

---

## 6. Arsitektur Sistem

### 6.1 Arsitektur Level Tinggi

Aplikasi menggunakan arsitektur berlapis (layered architecture) yang memisahkan tanggung jawab antara antarmuka, logika aplikasi, dan model.

```
┌────────────────────────────────────────────────┐
│  Lapisan Antarmuka (Streamlit)                 │
│  app.py + pages/{prediksi, tentang}.py         │
└────────────────────┬───────────────────────────┘
                     │
┌────────────────────▼───────────────────────────┐
│  Lapisan Logika Aplikasi                       │
│  utils/{preprocessing, predictor, crawler,     │
│         styles}.py                             │
└────────────────────┬───────────────────────────┘
                     │
┌────────────────────▼───────────────────────────┐
│  Lapisan Model                                 │
│  model/{model_def.py, checkpoint.pt}           │
└────────────────────┬───────────────────────────┘
                     │
┌────────────────────▼───────────────────────────┐
│  Lapisan Sumber Daya                           │
│  assets/kamus/  +  model/tokenizer_cache/      │
└────────────────────────────────────────────────┘
```

### 6.2 Struktur Direktori

```
streamlit-mbg-bert-cnn/
├── app.py                     # Entry point + st.navigation()
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml            # Konfigurasi tema Streamlit
├── model/
│   ├── model_def.py           # Definisi kelas IndoBERTCNN
│   ├── indobert_cnn_dualpath_S2.pt   # Checkpoint model
│   └── tokenizer_cache/       # Cache tokenizer offline
├── utils/
│   ├── predictor.py           # Load model + inference
│   ├── preprocessing.py       # Pipeline preprocessing 4 tahap
│   ├── crawler.py             # Integrasi tweet-harvest
│   └── styles.py              # CSS global + komponen tampilan
├── pages/
│   ├── prediksi.py            # Halaman utama prediksi
│   └── tentang.py             # Halaman project showcase
└── assets/
    ├── sample_data.csv        # 10 tweet MBG terkurasi
    └── kamus/                 # Kamus preprocessing custom
        ├── kamus_alay_mbg.csv
        ├── demoji_code_mbg.csv
        ├── akun_x_mbg.csv
        ├── whitelist_hashtag_mbg.csv
        └── additional_stopwords_mbg.csv
```

### 6.3 Peran Modul

| Modul                    | Tanggung Jawab                                                              |
| ------------------------ | --------------------------------------------------------------------------- |
| `app.py`                 | Entry point aplikasi, routing halaman via `st.navigation()`                 |
| `pages/prediksi.py`      | Halaman utama dengan 4 tab (Input Teks, CSV, Sample, Crawling)              |
| `pages/tentang.py`       | Halaman project showcase                                                    |
| `utils/preprocessing.py` | Pipeline preprocessing 4 tahap identik dengan pipeline training             |
| `utils/predictor.py`     | Load model checkpoint, inisialisasi tokenizer, dan fungsi inference         |
| `utils/crawler.py`       | Integrasi dengan `tweet-harvest` untuk live crawling data                   |
| `utils/styles.py`        | CSS global aplikasi dan komponen `render_result_card`                       |
| `model/model_def.py`     | Definisi arsitektur kelas `IndoBERTCNN` (Dual-Path)                         |
| `assets/kamus/`          | Kamus custom domain MBG (slang, emoji, akun, hashtag) untuk preprocessing   |

---

## 7. Spesifikasi Model

### 7.1 Arsitektur

Model **IndoBERT-CNN Dual-Path** menggabungkan dua representasi komplementer dari IndoBERT:

- **Path 1 - Konteks Global:** representasi token `[CLS]` dari IndoBERT dengan dropout regularization.
- **Path 2 - Pola N-gram Lokal:** CNN 1D multi-kernel dengan Global Max Pooling untuk menangkap pola sekuensial lokal.
- **Concatenation Layer:** menggabungkan output kedua path menjadi vektor dimensi 1.536.
- **Classifier Head:** rangkaian Dropout → Dense (ELU) → Dropout → Dense (Softmax) untuk klasifikasi 3 kelas.

### 7.2 Hyperparameter Final

| Parameter              | Nilai                             |
| ---------------------- | --------------------------------- |
| Backbone               | `indobenchmark/indobert-base-p2`  |
| Max Sequence Length    | 128 token                         |
| Kernel N-gram CNN      | `[1, 2, 3]`                       |
| Filter Size CNN        | 256                               |
| Activation Function    | ELU                               |
| Dense Size             | 256                               |
| Dropout (CLS)          | 0.1                               |
| Dropout (Head)         | 0.5                               |
| Learning Rate BERT     | 1 × 10⁻⁵                          |
| Learning Rate CNN      | 1 × 10⁻⁴                          |
| Batch Size             | 32                                |
| Weight Decay           | 0.01                              |
| Metode Validasi        | 5-Fold Stratified Cross-Validation |
| Kondisi Data           | Random Undersampling (S2)         |

### 7.3 Label Mapping

| ID | Label      |
| -- | ---------- |
| 0  | `positive` |
| 1  | `negative` |
| 2  | `neutral`  |

### 7.4 Format Checkpoint

Model checkpoint (`indobert_cnn_dualpath_S2.pt`) tersimpan sebagai dictionary yang berisi:

- `model_state_dict`: bobot model
- `label2id` dan `id2label`: mapping label
- `bert_model_name`: identifier backbone
- `cnn_config`: konfigurasi arsitektur CNN
- `lr_config`, `fixed_config`: metadata training
- `test_metrics`, `per_class_f1`: performa evaluasi

---

## 8. Spesifikasi Data

### 8.1 Dataset Training

| Atribut               | Nilai                                          |
| --------------------- | ---------------------------------------------- |
| Sumber Data           | Platform X (Twitter)                           |
| Bahasa                | Bahasa Indonesia                               |
| Kata Kunci            | `makan bergizi gratis`, `mbg`                  |
| Periode Crawling      | Januari 2025 sampai Januari 2026               |
| Total Data Mentah     | 172.009 tweet                                  |
| Total Data Berlabel   | 6.642 tweet                                    |
| Distribusi Kelas      | Positif 2.625 (39,5%); Negatif 2.085 (31,4%); Netral 1.932 (29,1%) |
| Split Train + Val     | 5.313 tweet (80%)                              |
| Split Test            | 1.329 tweet (20%, fixed)                       |

### 8.2 Sample Data Aplikasi

Aplikasi menyertakan `assets/sample_data.csv` berisi 10 tweet terkurasi dengan variasi topik terkait Program MBG untuk keperluan demonstrasi cepat.

---

## 9. Pipeline Preprocessing

Preprocessing pada aplikasi identik dengan pipeline preprocessing pada tahap training untuk memastikan konsistensi hasil prediksi. Pipeline terdiri dari empat tahap yang dijalankan secara berurutan.

### 9.1 Tahap 1 - Case Folding dan HTML Unescape

- Normalisasi seluruh huruf menjadi huruf kecil.
- Decoding entitas HTML umum (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`).

### 9.2 Tahap 2 - Cleaning

- Penghapusan URL, mention, dan hashtag non-whitelist.
- Konversi emoji menjadi frasa Bahasa Indonesia (kamus `demoji_code_mbg.csv`).
- Normalisasi format mata uang, tanggal, dan angka.
- Konversi emotikon ASCII menjadi kata (misal `:)` → `senang`).
- Normalisasi repetisi huruf berlebih (misal `enaakkk` → `enak`).

### 9.3 Tahap 3 - Tokenization

- Pemisahan teks berdasarkan whitespace sebagai helper untuk tahap normalization.

### 9.4 Tahap 4 - Normalization

- Normalisasi slang berdasarkan kamus Nasal (`colloquial-indonesian-lexicon`) dan kamus custom domain MBG.
- Penanganan negasi (misal `gak`, `nggak` → `tidak`).
- Deduplikasi frasa berulang.
- Output: kolom `text_bert` siap untuk tokenisasi IndoBERT.

---

## 10. Non-Functional Requirements

### NFR-1: Performa

| Metrik                       | Target                                                       |
| ---------------------------- | ------------------------------------------------------------ |
| Cold start (model load)      | Kurang dari 15 detik pertama kali                            |
| Warm inference (single text) | Kurang dari 1 detik pada akselerator, kurang dari 3 detik pada CPU |
| Batch 500 baris              | Kurang dari 60 detik pada akselerator                        |

**Strategi:** Auto-deteksi device (MPS > CUDA > CPU), caching tokenizer offline melalui `model/tokenizer_cache/`, dan warm-up model saat aplikasi pertama kali dimuat.

### NFR-2: Kompatibilitas

| Aspek           | Dukungan                                        |
| --------------- | ----------------------------------------------- |
| Python          | 3.9 dan versi lebih baru                        |
| Sistem Operasi  | Windows, macOS, Linux                           |
| Browser         | Chrome, Firefox, Safari, Edge (versi modern)    |
| Akselerator     | Apple Silicon MPS, NVIDIA CUDA, atau CPU        |

### NFR-3: Reproducibility

- Pipeline preprocessing pada aplikasi harus identik dengan pipeline preprocessing pada training (menghindari train-serve skew).
- Model checkpoint self-contained dengan seluruh metadata konfigurasi dalam satu file.
- Tokenizer di-cache secara offline untuk menjamin konsistensi antara environment training dan runtime.

### NFR-4: Input Validation

| Input           | Batasan                                          |
| --------------- | ------------------------------------------------ |
| Teks tunggal    | Maksimal 512 karakter                            |
| File CSV        | Maksimal 10 MB, 500 baris untuk prediksi         |
| Auth token X    | String cookie `auth_token` valid                 |
| Crawling limit  | 10 sampai 500 tweet per sesi                     |

### NFR-5: User Experience

- Antarmuka menggunakan Bahasa Indonesia sepenuhnya.
- Layout responsif untuk resolusi desktop dan tablet.
- Feedback visual selama proses asynchronous (loading, progress, completion).
- Result card yang informatif dengan hierarki visual yang jelas.
- Konsistensi warna, tipografi, dan komponen di seluruh halaman.

### NFR-6: Ekstensibilitas

- Modul preprocessing dapat diperbarui melalui file kamus pada `assets/kamus/` tanpa mengubah kode aplikasi.
- Model checkpoint dapat diganti melalui penempatan file `.pt` baru pada folder `model/` sesuai format checkpoint standar.
- Struktur multi-page mendukung penambahan halaman baru melalui folder `pages/`.

---

## 11. Success Metrics

### 11.1 Performa Model

Evaluasi pada test set fixed sebanyak 1.329 tweet:

| Metrik            | Nilai      |
| ----------------- | ---------- |
| Accuracy          | 85,70%     |
| F1-Macro          | 0,8547     |
| F1-Weighted       | 0,8587     |
| Precision (Macro) | 0,8551     |
| Recall (Macro)    | 0,8585     |
| F1 Kelas Positif  | 0,8891     |
| F1 Kelas Negatif  | 0,8717     |
| F1 Kelas Netral   | 0,8034     |

### 11.2 Validasi K-Fold

Hasil 5-Fold Stratified Cross-Validation pada train+val (kondisi S2 Random Undersampling): **F1-Macro rata-rata 0,846 ± 0,016**.

### 11.3 Ketepatan Fungsional

- Seluruh mode input (teks tunggal, batch CSV, sample, crawling) menghasilkan prediksi konsisten pada input yang sama.
- Preprocessing pada aplikasi menghasilkan `text_bert` yang identik dengan preprocessing pada training.
- Result card menampilkan probabilitas yang berjumlah 1.0 untuk setiap prediksi.

---

## 12. Tech Stack dan Dependensi

### 12.1 Dependensi Python

| Kategori              | Pustaka                       | Versi Minimal |
| --------------------- | ----------------------------- | ------------- |
| Framework Aplikasi    | Streamlit                     | 1.35          |
| Deep Learning         | PyTorch                       | 2.0           |
| NLP                   | Transformers (HuggingFace)    | 4.40          |
| Pengolahan Data       | pandas                        | 2.0           |
| Komputasi Numerik     | numpy                         | 1.24          |
| Visualisasi           | Plotly                        | 5.18          |
| Tokenisasi            | sentencepiece, protobuf       | terbaru       |
| HTTP Client           | requests                      | terbaru       |

### 12.2 Dependensi Sistem (untuk fitur Crawling)

| Komponen         | Versi Minimal | Kegunaan                          |
| ---------------- | ------------- | --------------------------------- |
| Node.js          | 18            | Runtime `tweet-harvest`           |
| tweet-harvest    | 2.7.1         | Library crawling Twitter/X        |
| Playwright       | 1.41.1        | Browser automation (auto-install) |

---

## 13. Deployment dan Environment

### 13.1 Target Deployment

Aplikasi dirancang untuk berjalan pada **lingkungan lokal** pengguna (laptop, workstation, atau VM) yang mendukung akses shell dan runtime Python + Node.js.

### 13.2 Prasyarat Perangkat Keras

| Komponen         | Minimal                                  |
| ---------------- | ---------------------------------------- |
| Prosesor         | 4 core, 2,0 GHz                          |
| RAM              | 8 GB                                     |
| Penyimpanan      | 2 GB kosong                              |
| Akselerator      | Opsional (NVIDIA CUDA atau Apple MPS)    |

### 13.3 Instalasi

```bash
# 1. Clone repositori
git clone https://github.com/roziqinkhoeru/streamlit-mbg-bert-cnn.git
cd streamlit-mbg-bert-cnn

# 2. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# 3. Instalasi dependensi
pip install -r requirements.txt

# 4. Tempatkan model checkpoint di folder model/
# File: indobert_cnn_dualpath_S2.pt

# 5. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis pada browser di `http://localhost:8501`.

---

## 14. Referensi

### 14.1 Model dan Pustaka

- **IndoBERT Base P2** - `indobenchmark/indobert-base-p2` ([HuggingFace](https://huggingface.co/indobenchmark/indobert-base-p2))
- **tweet-harvest** - Helmi Satria ([GitHub](https://github.com/helmisatria/tweet-harvest))
- **Nasal Colloquial Indonesian Lexicon** - Salsabila et al. ([GitHub](https://github.com/nasalsabila/kamus-alay))

### 14.2 Penelitian Terkait

- Devlin et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*.
- Kim (2014). *Convolutional Neural Networks for Sentence Classification*.
- Koto et al. (2020). *IndoLEM and IndoBERT: A Benchmark Dataset and Pre-trained Language Model for Indonesian NLP*.

### 14.3 Repositori Penelitian

- Kode penelitian pipeline: [github.com/roziqinkhoeru/mbg_bertn_cnn](https://github.com/roziqinkhoeru/mbg_bertn_cnn)
- Repositori data lengkap: [bit.ly/codembgbecnn](https://bit.ly/codembgbecnn)

---

**Dokumen ini mendefinisikan spesifikasi produk SentiMBG versi 1.0.**  
**Departemen Informatika, Fakultas Sains dan Matematika, Universitas Diponegoro.**
