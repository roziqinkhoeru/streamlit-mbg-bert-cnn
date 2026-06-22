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
├── model/
│   ├── model_def.py
│   └── indobert_cnn_dualpath_S2.pt   ← LETAKKAN MODEL DI SINI
├── utils/
│   ├── predictor.py
│   └── styles.py
└── pages/
    ├── dashboard.py
    ├── prediksi.py
    └── tentang.py
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

## Model

- File: `model/indobert_cnn_dualpath_S2.pt`
- Backbone: `indobenchmark/indobert-base-p2`
- Arsitektur: Dual-Path [CLS] + CNN 1D
- F1-Macro: 0.8547 | Accuracy: 85.70%
