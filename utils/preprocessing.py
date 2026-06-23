"""
utils/preprocessing.py
Pipeline preprocessing teks untuk SentiMBG — identik dengan NB02.

Menghasilkan text_bert (Step 1-4):
  Step 1 → Case Folding & HTML Unescape
  Step 2 → Cleaning (URL, mention, emoji, hashtag, currency, karakter)
  Step 3 → Tokenization (whitespace split — parsing helper)
  Step 4 → Normalization (slang, negasi, dedup) → OUTPUT: text_bert

PENTING: Pipeline ini harus identik dengan NB02 karena model dilatih
         menggunakan kolom text_bert, BUKAN full_text.
         Mengirim teks mentah ke model akan menghasilkan train-serve skew.

Dependensi kamus:
  - colloquial-indonesian-lexicon.csv  (Nasal, di-download otomatis)
  - assets/kamus/kamus_alay_mbg.csv   (opsional, domain MBG custom)
  - assets/kamus/demoji_code_mbg.csv  (opsional)
  - assets/kamus/akun_x_mbg.csv       (opsional)
  - assets/kamus/whitelist_hashtag_mbg.csv (opsional)

Jika file kamus tidak ditemukan, pipeline tetap berjalan menggunakan
Nasal saja (fallback graceful) — tidak ada crash.
"""

import os
import re
import requests
import pandas as pd
import streamlit as st

# ── Path kamus ────────────────────────────────────────────────────────────────
_ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_KAMUS_DIR  = os.path.join(_ROOT, "assets", "kamus")
_NASAL_URL  = "https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv"
_NASAL_PATH = os.path.join(_KAMUS_DIR, "colloquial-indonesian-lexicon.csv")

# Kata yang TIDAK BOLEH diubah oleh kamus alay (singkatan protected)
_PROTECTED_WORDS = {'sma', 'smp', 'sd', 'tk', 'pt'}


def _load_csv_safe(filename, required_cols=None):
    """Load CSV dari folder kamus. Return DataFrame kosong jika tidak ada."""
    path = os.path.join(_KAMUS_DIR, filename)
    if not os.path.exists(path):
        return pd.DataFrame(columns=required_cols or ['original_term', 'replacement'])
    try:
        return pd.read_csv(path, on_bad_lines='skip')
    except Exception:
        return pd.DataFrame(columns=required_cols or ['original_term', 'replacement'])


def _ensure_nasal(force_download=False):
    """
    Pastikan kamus Nasal tersedia lokal.
    Download sekali jika belum ada, lalu cache di assets/kamus/.
    """
    os.makedirs(_KAMUS_DIR, exist_ok=True)
    if not os.path.exists(_NASAL_PATH) or force_download:
        try:
            r = requests.get(_NASAL_URL, timeout=15)
            r.raise_for_status()
            with open(_NASAL_PATH, "wb") as f:
                f.write(r.content)
        except Exception:
            # Jika download gagal, kembalikan dict kosong — pipeline tetap jalan
            return {}
    try:
        df = pd.read_csv(_NASAL_PATH)
        return {
            str(k).lower(): str(v).lower()
            for k, v in zip(df['slang'], df['formal'])
            if pd.notna(k) and pd.notna(v)
        }
    except Exception:
        return {}


@st.cache_resource(show_spinner=False)
def _load_all_dicts():
    """
    Load & build semua dictionary preprocessing.
    Di-cache oleh Streamlit — hanya dijalankan sekali per sesi.
    """
    os.makedirs(_KAMUS_DIR, exist_ok=True)

    # ── Load kamus Nasal (download jika belum ada) ────────────────────────────
    nasal_dict = _ensure_nasal()

    # ── Load kamus custom domain MBG ─────────────────────────────────────────
    df_alay   = _load_csv_safe('kamus_alay_mbg.csv')
    df_demoji = _load_csv_safe('demoji_code_mbg.csv')
    df_akun   = _load_csv_safe('akun_x_mbg.csv')
    df_wl     = _load_csv_safe('whitelist_hashtag_mbg.csv')

    # ── Bangun dict emoji ─────────────────────────────────────────────────────
    dict_demoji = {
        str(k).strip(): str(v).strip()
        for k, v in zip(
            df_demoji.get('original_term', pd.Series([], dtype=str)),
            df_demoji.get('replacement',   pd.Series([], dtype=str))
        )
        if pd.notna(k) and pd.notna(v) and str(k).strip() != ''
    }

    # ── Bangun dict akun penting ──────────────────────────────────────────────
    dict_akun = {
        str(k).strip(): str(v).strip()
        for k, v in zip(
            df_akun.get('original_term', pd.Series([], dtype=str)),
            df_akun.get('replacement',   pd.Series([], dtype=str))
        )
        if pd.notna(k) and pd.notna(v)
    }

    # ── Bangun whitelist hashtag ──────────────────────────────────────────────
    whitelist_hashtags = set(
        df_wl['hashtag'].astype(str).str.lower().str.strip().tolist()
    ) if not df_wl.empty and 'hashtag' in df_wl.columns else set()

    # ── Merge kamus alay: Nasal sebagai base, custom sebagai override ─────────
    full_dict_alay = dict(nasal_dict)  # copy dari Nasal

    dict_custom = {
        str(k).lower(): str(v).lower()
        for k, v in zip(
            df_alay.get('original_term', pd.Series([], dtype=str)),
            df_alay.get('replacement',   pd.Series([], dtype=str))
        )
        if pd.notna(k) and pd.notna(v)
    }
    full_dict_alay.update(dict_custom)  # custom override Nasal

    # ── Proteksi kata yang tidak boleh diubah ─────────────────────────────────
    for word in _PROTECTED_WORDS:
        full_dict_alay.pop(word, None)

    # ── Pisahkan frasa vs kata tunggal ────────────────────────────────────────
    dict_phrases   = {k: v for k, v in full_dict_alay.items() if ' ' in k}
    dict_words     = {k: v for k, v in full_dict_alay.items() if ' ' not in k}
    sorted_phrases = sorted(dict_phrases.keys(), key=len, reverse=True)

    return {
        'dict_demoji'     : dict_demoji,
        'dict_akun'       : dict_akun,
        'whitelist_hashtags': whitelist_hashtags,
        'dict_phrases'    : dict_phrases,
        'dict_words'      : dict_words,
        'sorted_phrases'  : sorted_phrases,
        'nasal_size'      : len(nasal_dict),
        'custom_size'     : len(dict_custom),
    }


# ════════════════════════════════════════════════════════════════════
#  STEP 1 — CASE FOLDING & HTML UNESCAPE
# ════════════════════════════════════════════════════════════════════

def _step1_casefolding(text: str) -> str:
    """Lowercase + decode HTML entities umum di Twitter/X."""
    if not text or str(text).strip() == '':
        return ''
    temp = str(text)
    temp = temp.replace('&amp;',  ' dan ')
    temp = temp.replace('&lt;',   ' kurang dari ')
    temp = temp.replace('&gt;',   ' lebih dari ')
    temp = temp.replace('&quot;', '"')
    temp = temp.replace('&#39;',  "'")
    return temp.lower()


# ════════════════════════════════════════════════════════════════════
#  STEP 2 — CLEANING
# ════════════════════════════════════════════════════════════════════

def _step2_cleaning(text: str, dicts: dict) -> str:
    """Pembersihan menyeluruh dengan mempertahankan sinyal sentimen."""
    if not text:
        return ''
    temp = text

    dict_demoji      = dicts['dict_demoji']
    dict_akun        = dicts['dict_akun']
    whitelist_hashtags = dicts['whitelist_hashtags']

    # 2.1 Emotikon teks ASCII
    temp = re.sub(r'[:;=x][\-~]?[)d\]]+', ' senang ', temp)
    temp = re.sub(r'[:;=x][\-~]?[(\[]+',  ' sedih ',  temp)

    # 2.2 Hapus URL
    temp = re.sub(r'http\S+|www\S+|https\S+', ' ', temp, flags=re.MULTILINE)

    # 2.3 Singkatan domain dalam kurung
    for pat in [r'\(\s*mbg\s*\)', r'\(\s*bgn\s*\)',
                r'\(\s*apbn\s*\)', r'\(\s*as\s*\)']:
        temp = re.sub(pat, ' ', temp)

    # 2.4 Normalisasi whitespace & newline
    temp = temp.replace('\n', ' . ')
    temp = re.sub(r'[\t\xa0]', ' ', temp)
    temp = re.sub(r'([?!,.])(?=[a-z#])', r'\1 ', temp)

    # 2.5 Normalisasi suffix slang possesif (otak'nya → otaknya)
    temp = re.sub(r"(?<=[a-z])['`]+[ya]\b", 'nya', temp)

    # 2.6 Penyelamat huruf tunggal (s-nya → huruf s nya)
    temp = re.sub(r"\b([a-z])(?:-|'|\s)*nya\b", r'huruf \1 nya', temp)

    # 2.7 Pemangkas repetisi huruf berlebih (enaaaaak → enak)
    temp = re.sub(r'([a-z])\1{2,}', r'\1', temp)

    # 2.8 Hashtag: whitelist → pertahankan teks, non-whitelist → hapus
    for tag in re.findall(r'#\w+', temp):
        clean_tag = tag.lower().lstrip('#')
        if clean_tag in whitelist_hashtags or tag.lower() in whitelist_hashtags:
            temp = temp.replace(tag, ' ' + tag[1:] + ' ')
        else:
            temp = temp.replace(tag, ' ')

    # 2.9 Mention: penting → nama asli (kamus), sisanya hapus
    for k, v in dict_akun.items():
        temp = re.sub(re.escape(k), ' ' + v + ' ', temp, flags=re.IGNORECASE)
    temp = re.sub(r'@\w+', ' ', temp)

    # 2.10 Emoji → frasa (kamus custom frequency-based)
    for k, v in dict_demoji.items():
        temp = temp.replace(k, ' ' + v + ' ')

    # 2.11 Normalisasi kata ulang angka (anak2 → anak anak)
    temp = re.sub(
        r'\b([a-z]{2,})2(nya|ny|ku|mu|an|in|kan|san|kah|lah|pun|)\b',
        r'\1 \1\2', temp
    )

    # 2.12 Currency shield
    temp = re.sub(r'\b(?:rp|rupiah)\s*[.,]?\s*(\d)', r'rp \1', temp)

    def _ubah_mata_uang(m):
        angka  = m.group(1).replace(' ', ',')
        suffix = m.group(2)
        peta   = {
            'k': 'ribu', 'rb': 'ribu', 'ribu': 'ribu',
            'jt': 'juta', 'juta': 'juta',
            'm': 'miliar', 'miliar': 'miliar', 'milyar': 'miliar',
            't': 'triliun', 'triliun': 'triliun', 'triliyun': 'triliun',
            'perak': 'rupiah'
        }
        return f"{angka} {peta[suffix]}"

    temp = re.sub(
        r'\b(\d+(?:[.,\s]\d+)?)\s*'
        r'(k|rb|ribu|jt|juta|m|miliar|milyar|t|triliun|triliyun|perak)\b',
        _ubah_mata_uang, temp
    )
    temp = re.sub(
        r'\b(\d{1,3}(?:\.\d{3})+)\b',
        lambda m: m.group(1).replace('.', ''), temp
    )

    # 2.13 Hapus format tanggal numerik
    temp = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', ' ', temp)
    _bulan = (r'(januari|februari|maret|april|mei|juni|juli|'
              r'agustus|september|oktober|november|desember)')
    temp = re.sub(rf'\b\d{{1,2}}\s+{_bulan}\s+\d{{2,4}}\b', ' tanggal ', temp)
    temp = re.sub(r'\b\d{1,2}[:.\\-]\d{2}(?:[:.\\-]\d{2})?\b', ' ', temp)

    # 2.14 Pecahan & persen
    temp = re.sub(r'(?<!\w)1/2(?!\w)', ' setengah ',   temp)
    temp = re.sub(r'(?<!\w)1/3(?!\w)', ' sepertiga ',  temp)
    temp = re.sub(r'(?<!\w)1/4(?!\w)', ' seperempat ', temp)
    temp = re.sub(r'(?<!\w)3/4(?!\w)', ' tiga perempat ', temp)
    temp = re.sub(r'(?<!\w)(\d+)/(\d+)(?!\w)', r'\1 per \2', temp)
    temp = temp.replace('%', ' persen ')

    # 2.15 Normalisasi tanda baca berlebih
    temp = re.sub(r'\.{3,}', ' ... ', temp)
    temp = re.sub(r'(?<!\.)\.\.(?!\.)', ' . ', temp)
    temp = re.sub(r'[^a-z0-9\s\?\!\,\.]', ' ', temp)

    # Pisahkan tanda baca yang berbatasan dengan huruf
    temp = re.sub(r'([a-z])([?!,\.]+)', r'\1 \2', temp)
    temp = re.sub(r'([?!,\.]+)([a-z])', r'\1 \2', temp)

    return re.sub(r'\s+', ' ', temp).strip()


# ════════════════════════════════════════════════════════════════════
#  STEP 3 — TOKENIZATION (parsing helper)
# ════════════════════════════════════════════════════════════════════

def _step3_tokenization(text: str) -> str:
    """Whitespace split sebagai parsing helper untuk Step 4."""
    if not text:
        return ''
    return ' '.join(text.split())


# ════════════════════════════════════════════════════════════════════
#  STEP 4 — NORMALIZATION → OUTPUT: text_bert
# ════════════════════════════════════════════════════════════════════

def _step4_normalization(text: str, dicts: dict) -> str:
    """Normalisasi slang, negasi, dedup frasa → menghasilkan text_bert."""
    if not text:
        return ''

    dict_phrases   = dicts['dict_phrases']
    dict_words     = dicts['dict_words']
    sorted_phrases = dicts['sorted_phrases']

    temp = ' ' + text + ' '

    # 4.1 Normalisasi frasa (longest match first)
    for phrase in sorted_phrases:
        if phrase in temp:
            temp = re.sub(
                r'\b' + re.escape(phrase) + r'\b',
                ' ' + dict_phrases[phrase] + ' ', temp
            )

    # 4.2 Normalisasi kata tunggal
    tokens = temp.split()
    temp   = ' '.join([dict_words.get(w, w) for w in tokens])

    # 4.3 Normalisasi negasi (word boundary ketat)
    temp = re.sub(r'\bnggak\b', 'tidak', temp)
    temp = re.sub(r'\bngga\b',  'tidak', temp)
    temp = re.sub(r'\bgak\b',   'tidak', temp)
    temp = re.sub(r'\bga\b',    'tidak', temp)

    # 4.4 Dedup frasa hasil ekspansi whitelist/kamus
    for phrase in ['makan bergizi gratis', 'badan gizi nasional',
                   'anggaran pendapatan dan belanja negara']:
        temp = re.sub(
            rf'\b({re.escape(phrase)})(\s+\1)+\b', r'\1', temp
        )

    # Rapatkan kembali tanda baca
    temp = re.sub(r'\s+([?!,\.])', r'\1', temp)

    return re.sub(r'\s+', ' ', temp).strip()


# ════════════════════════════════════════════════════════════════════
#  MASTER PIPELINE — PUBLIC API
# ════════════════════════════════════════════════════════════════════

def preprocess(text: str) -> str:
    """
    Pipeline preprocessing lengkap (Step 1–4) identik dengan NB02.

    Input : teks mentah dari user (full_text / input manual)
    Output: text_bert — siap untuk tokenizer IndoBERT

    Gunakan fungsi ini di Streamlit SEBELUM memanggil tokenizer.
    """
    dicts = _load_all_dicts()
    s1 = _step1_casefolding(text)
    s2 = _step2_cleaning(s1, dicts)
    s3 = _step3_tokenization(s2)
    s4 = _step4_normalization(s3, dicts)
    return s4


def get_preprocessing_info() -> dict:
    """
    Kembalikan info status kamus yang ter-load.
    Berguna untuk debugging atau tampilan info di UI.
    """
    try:
        dicts = _load_all_dicts()
        return {
            'nasal_entries'     : dicts['nasal_size'],
            'custom_entries'    : dicts['custom_size'],
            'phrase_entries'    : len(dicts['dict_phrases']),
            'word_entries'      : len(dicts['dict_words']),
            'emoji_entries'     : len(dicts['dict_demoji']),
            'akun_entries'      : len(dicts['dict_akun']),
            'whitelist_entries' : len(dicts['whitelist_hashtags']),
            'status'            : 'ok',
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
