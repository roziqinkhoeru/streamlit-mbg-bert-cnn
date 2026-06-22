"""
predictor.py
Load model dan fungsi inference untuk aplikasi Streamlit.
Menggunakan @st.cache_resource agar model hanya di-load sekali.

Optimasi cold-start:
- Tokenizer di-save lokal ke model/tokenizer_cache/ saat pertama run
- Selanjutnya load dari disk, tidak perlu download HuggingFace lagi
"""

import os
import sys
import torch
import streamlit as st
import numpy as np
from transformers import AutoTokenizer

# Tambahkan root project ke path agar import model_def bisa ditemukan
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from model.model_def import IndoBERTCNN

# ── Konfigurasi model (harus identik dengan saat training) ───────────────────
BERT_MODEL_NAME  = "indobenchmark/indobert-base-p2"
NUM_CLASSES      = 3
NGRAM_SIZES      = [1, 2, 3]
FILTER_SIZE      = 256
DROPOUT          = 0.5
ACTIVATION       = "elu"
CLS_DROPOUT      = 0.1
DENSE_SIZE       = 256
MAX_LEN          = 128

# Label mapping — identik dengan notebook
ID2LABEL    = {0: "positive", 1: "negative", 2: "neutral"}
LABEL2ID    = {"positive": 0, "negative": 1, "neutral": 2}
LABEL_NAMES = ["positive", "negative", "neutral"]

# Path
MODEL_PATH      = os.path.join(ROOT, "model", "indobert_cnn_dualpath_S2.pt")
TOKENIZER_CACHE = os.path.join(ROOT, "model", "tokenizer_cache")


def get_device():
    """Pilih device terbaik: MPS (Apple Silicon) > CUDA > CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def _load_tokenizer():
    """
    Load tokenizer dari cache lokal jika ada,
    otherwise download dari HuggingFace lalu simpan lokal.
    Ini menghilangkan network call saat cold start berikutnya.
    """
    if os.path.isdir(TOKENIZER_CACHE) and os.listdir(TOKENIZER_CACHE):
        # Load dari disk — jauh lebih cepat
        return AutoTokenizer.from_pretrained(TOKENIZER_CACHE, local_files_only=True)
    else:
        # Download sekali, simpan lokal
        os.makedirs(TOKENIZER_CACHE, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
        tokenizer.save_pretrained(TOKENIZER_CACHE)
        return tokenizer


@st.cache_resource(show_spinner=False)
def load_model_and_tokenizer():
    """
    Load model IndoBERTCNN dan tokenizer.
    Di-cache oleh Streamlit — hanya dijalankan sekali per sesi app.
    Mengembalikan (model, tokenizer, device) atau raise Exception jika gagal.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"File model tidak ditemukan: {MODEL_PATH}\n"
            "Pastikan file 'indobert_cnn_dualpath_S2.pt' ada di folder 'model/'"
        )

    device = get_device()

    # Load tokenizer (dari cache lokal jika sudah pernah run)
    tokenizer = _load_tokenizer()

    # Bangun arsitektur model
    model = IndoBERTCNN(
        bert_model_name=BERT_MODEL_NAME,
        num_classes=NUM_CLASSES,
        ngram_sizes=NGRAM_SIZES,
        filter_size=FILTER_SIZE,
        dropout=DROPOUT,
        activation=ACTIVATION,
        cls_dropout=CLS_DROPOUT,
        dense_size=DENSE_SIZE,
    )

    # Load weights dari .pt — map ke CPU dulu, biarkan get_device() handle device
    # PyTorch 2.6+ default weights_only=True menolak unpickle beberapa tipe numpy
    # (numpy scalar, numpy.dtype, dst.) yang ada di checkpoint ini. Karena file
    # ini adalah checkpoint hasil training sendiri (trusted), aman pakai weights_only=False.
    checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    state_dict = checkpoint["model_state_dict"] if "model_state_dict" in checkpoint else checkpoint
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # Warm-up: satu forward pass dummy agar MPS/CPU graph sudah terkompilasi
    _warmup(model, tokenizer, device)

    return model, tokenizer, device


def _warmup(model, tokenizer, device):
    """
    Satu forward pass dengan input dummy.
    Ini memaksa PyTorch mengompilasi graph lebih awal
    sehingga prediksi pertama pengguna tidak terasa lambat.
    """
    dummy = tokenizer(
        "tes",
        max_length=MAX_LEN,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    with torch.no_grad():
        model(dummy["input_ids"].to(device), dummy["attention_mask"].to(device))


def predict_single(text: str, model, tokenizer, device) -> dict:
    """
    Prediksi sentimen untuk satu teks.

    Returns:
        {
            "label": str,           # "positive" / "negative" / "neutral"
            "label_id": int,        # 0 / 1 / 2
            "confidence": float,    # 0.0-1.0
            "probs": list[float],   # [prob_pos, prob_neg, prob_neu]
        }
    """
    text = text.strip()
    if not text:
        raise ValueError("Teks tidak boleh kosong.")

    encoding = tokenizer(
        text,
        max_length=MAX_LEN,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )

    input_ids      = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probs  = torch.softmax(logits, dim=1).squeeze().cpu().numpy()

    label_id   = int(np.argmax(probs))
    confidence = float(probs[label_id])

    return {
        "label":      ID2LABEL[label_id],
        "label_id":   label_id,
        "confidence": confidence,
        "probs":      probs.tolist(),
    }


def predict_batch(texts: list, model, tokenizer, device, progress_callback=None) -> list:
    """
    Prediksi sentimen untuk list teks.
    progress_callback(i, total) dipanggil setiap iterasi.
    """
    results = []
    for i, text in enumerate(texts):
        try:
            result = predict_single(str(text), model, tokenizer, device)
        except Exception:
            result = {
                "label":      "neutral",
                "label_id":   2,
                "confidence": 0.0,
                "probs":      [0.0, 0.0, 1.0],
            }
        results.append(result)
        if progress_callback:
            progress_callback(i + 1, len(texts))
    return results
