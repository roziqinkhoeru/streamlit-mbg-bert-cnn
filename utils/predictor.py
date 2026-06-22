"""
predictor.py
Load model dan fungsi inference untuk aplikasi Streamlit.
Menggunakan @st.cache_resource agar model hanya di-load sekali.
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
BERT_MODEL_NAME = "indobenchmark/indobert-base-p2"
NUM_CLASSES     = 3
NGRAM_SIZES     = [1, 2, 3]
FILTER_SIZE     = 256
DROPOUT         = 0.5
ACTIVATION      = "elu"
CLS_DROPOUT     = 0.1
DENSE_SIZE      = 256
MAX_LEN         = 128

# Label mapping — identik dengan notebook
ID2LABEL = {0: "positive", 1: "negative", 2: "neutral"}
LABEL2ID = {"positive": 0, "negative": 1, "neutral": 2}
LABEL_NAMES = ["positive", "negative", "neutral"]

# Path model checkpoint
MODEL_PATH = os.path.join(ROOT, "model", "indobert_cnn_dualpath_S2.pt")


def get_device():
    """Pilih device terbaik: MPS (Apple Silicon) > CUDA > CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


@st.cache_resource(show_spinner=False)
def load_model_and_tokenizer():
    """
    Load model IndoBERTCNN dan tokenizer.
    Di-cache oleh Streamlit — hanya dijalankan sekali per sesi.
    Mengembalikan (model, tokenizer, device) atau raise Exception jika gagal.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"File model tidak ditemukan: {MODEL_PATH}\n"
            "Pastikan file 'indobert_cnn_dualpath_S2.pt' ada di folder 'model/'"
        )

    device = get_device()

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

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

    # Load weights
    state_dict = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    return model, tokenizer, device


def predict_single(text: str, model, tokenizer, device) -> dict:
    """
    Prediksi sentimen untuk satu teks.

    Returns:
        {
            "label": str,           # "positive" / "negative" / "neutral"
            "label_id": int,        # 0 / 1 / 2
            "confidence": float,    # 0.0–1.0
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
        "probs":      probs.tolist(),   # [prob_pos, prob_neg, prob_neu]
    }


def predict_batch(texts: list, model, tokenizer, device, progress_callback=None) -> list:
    """
    Prediksi sentimen untuk list teks.
    progress_callback(i, total) dipanggil setiap iterasi — untuk progress bar Streamlit.

    Returns:
        list of dict (sama format dengan predict_single)
    """
    results = []
    total   = len(texts)

    for i, text in enumerate(texts):
        try:
            result = predict_single(str(text), model, tokenizer, device)
        except Exception:
            # Jika satu baris gagal, isi dengan nilai default
            result = {
                "label":      "neutral",
                "label_id":   2,
                "confidence": 0.0,
                "probs":      [0.0, 0.0, 1.0],
            }
        results.append(result)

        if progress_callback:
            progress_callback(i + 1, total)

    return results
