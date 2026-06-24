# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Streamlit demo app for a skripsi (undergraduate thesis): sentiment analysis of Indonesian X/Twitter
opinion about the "Makan Bergizi Gratis" (MBG) government program, using a custom IndoBERT-CNN
Dual-Path model. Two pages: **Home** (text/CSV/sample-data sentiment prediction) and **Tentang**
(project showcase — metrics, architecture, dataset, methodology, references).

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app.py
```

There is no test suite, linter, or build step configured in this project. Verify changes by booting
the app (`streamlit run app.py --server.headless true`) and checking the relevant page renders without
exceptions, and/or by exercising `utils/predictor.py` functions directly via a one-off Python script.

The model checkpoint (`model/indobert_cnn_dualpath_S2.pt`) is git-ignored and must be placed manually —
the app raises `FileNotFoundError` with setup instructions if it's missing.

## Architecture

### Page routing
`app.py` is the sole entry point. It uses **`st.navigation()`/`st.Page()`** (not the legacy `pages/`
auto-discovery) — this is intentional and load-bearing: Streamlit auto-scans any `pages/` directory
and generates a second, conflicting sidebar nav unless `st.navigation()` is explicitly called first.
Do not revert to manual `from pages.x import render` + a custom radio widget; that previously caused a
duplicated/broken sidebar. Page modules (`pages/prediksi.py`, `pages/tentang.py`) expose a parameterless
`render()` function passed directly to `st.Page(...)` as a callable, not a file path.

### Model loading & inference (`utils/predictor.py`)
- `load_model_and_tokenizer()` is `@st.cache_resource`-decorated — runs once per session, builds
  `IndoBERTCNN` (defined in `model/model_def.py`) and loads the checkpoint.
- The checkpoint is a **wrapper dict** (`{"model_state_dict": ..., "architecture": ..., "lr_config": ...,
  "cnn_config": ..., "fixed_config": ...}`), not a flat state_dict — always extract
  `checkpoint["model_state_dict"]` before `load_state_dict`.
- Loaded with `weights_only=False` deliberately. The checkpoint contains non-tensor numpy objects
  (`numpy.dtype`, numpy scalars) that PyTorch ≥2.6's default `weights_only=True` rejects; allowlisting
  every numpy type individually is impractical, and the checkpoint is the project's own trusted artifact.
- `predict_single()` always runs text through `utils/preprocessing.preprocess()` before tokenizing —
  the model was trained on a `text_bert` column, not raw `full_text`, so skipping preprocessing causes
  train-serve skew. If preprocessing collapses to <2 words, the original text is used as a fallback.
- Hardcoded model config constants (`NGRAM_SIZES`, `FILTER_SIZE`, `DROPOUT`, `ACTIVATION`, `CLS_DROPOUT`,
  `DENSE_SIZE`, `MAX_LEN`) must stay identical to training; they're also redundantly stored inside the
  checkpoint's `cnn_config`/`fixed_config` for reference.

### Model architecture (`model/model_def.py`)
`IndoBERTCNN` is a dual-path network: Path 1 takes the `[CLS]` token from IndoBERT's last hidden state
(global context), Path 2 runs multi-kernel 1D CNNs over the full sequence (local n-gram patterns); both
are concatenated before the classifier head. The CNN path *complements* `[CLS]`, it doesn't replace it.

### Preprocessing pipeline (`utils/preprocessing.py`)
A 4-step pipeline (case-folding → cleaning → tokenization → normalization) that must stay identical to
the training notebook (NB02), since the model expects exactly this normalization. Slang/emoji/account
dictionaries live in `assets/kamus/*.csv`; if a CSV is missing, the corresponding lookup degrades to
empty dict (no crash), except the Nasal colloquial-Indonesian lexicon, which auto-downloads on first run
and is cached at `assets/kamus/colloquial-indonesian-lexicon.csv`. `_load_all_dicts()` is
`@st.cache_resource`-decorated.

### Styling (`utils/styles.py`)
Single global CSS block injected via `inject_css()` (called at the top of every page's `render()`).
Dark theme; CSS vars defined in `:root`. Two gotchas if touching this file:
- `[data-testid="stIconMaterial"]` has an explicit font-family override — without it, the blanket
  `*, html, body { font-family: ... !important; }` rule clobbers Streamlit's Material icon font, and
  icons (including the sidebar collapse toggle) render as literal text like `keyboard_double_arrow_right`.
- Multi-line HTML passed to `st.markdown(..., unsafe_allow_html=True)` must avoid inconsistent
  indentation/blank lines — Streamlit's markdown parser can misinterpret indented HTML as a code block,
  causing stray literal tags (e.g. `</div>`) to render as visible text. Build HTML flush-left
  (see `render_result_card()` for the pattern: flat f-strings with no leading whitespace per line).

### CSV/batch prediction format
Pages that accept uploaded CSVs (Home → Upload CSV tab) expect a `full_text` column by convention
(falls back to the first column if absent) — this matches the output format of `tweet-harvest`
(Node.js/Playwright-based scraper), the tool actually used to collect this project's research dataset
(see `Fix Crawling MBG.ipynb`). There is no live-crawling feature in the app itself — it was removed;
only manual CSV upload and a small bundled sample dataset remain.
