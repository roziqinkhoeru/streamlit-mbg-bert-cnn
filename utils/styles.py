"""
styles.py
CSS global untuk tampilan dark professional AI.
Di-inject via st.markdown() di setiap halaman.
"""

GLOBAL_CSS = """
<style>
/* ── Google Fonts ────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ──────────────────────────────────── */
:root {
    --bg-primary:     #0D0F1A;
    --bg-card:        #141627;
    --bg-card-hover:  #1A1D35;
    --border:         #252842;
    --border-accent:  #6C63FF;
    --purple:         #6C63FF;
    --purple-light:   #8B83FF;
    --purple-dim:     rgba(108, 99, 255, 0.15);
    --green:          #10B981;
    --green-dim:      rgba(16, 185, 129, 0.15);
    --red:            #EF4444;
    --red-dim:        rgba(239, 68, 68, 0.15);
    --amber:          #F59E0B;
    --amber-dim:      rgba(245, 158, 11, 0.15);
    --text-primary:   #E8E9F3;
    --text-secondary: #9899B0;
    --text-muted:     #5A5C78;
    --font-main:      'Inter', sans-serif;
    --font-mono:      'JetBrains Mono', monospace;
    --radius:         10px;
    --radius-sm:      6px;
}

/* ── Base Reset ──────────────────────────────────────── */
*, html, body {
    font-family: var(--font-main) !important;
}

/* Material icon glyphs (sidebar toggle, alert icons, dst.) butuh font
   ligature khusus — kalau ikut ditimpa rule di atas, render jadi teks
   mentah (misal "keyboard_double_arrow_right") bukan simbol. */
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
}

/* ── Hide Streamlit branding, keep header (sidebar toggle lives there) ── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
}

/* ── Metric Cards ────────────────────────────────────── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 2px solid var(--purple);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    transition: border-color 0.15s;
}
.metric-card:hover {
    border-color: var(--border-accent);
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}
.metric-accent { color: var(--purple-light); }

/* ── Section Header ─────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1rem 0;
}
.section-dot {
    width: 6px; height: 24px;
    background: linear-gradient(180deg, var(--purple), var(--purple-light));
    border-radius: 3px;
    flex-shrink: 0;
}
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 0.01em;
}

/* ── Result Stat (kategori sentimen / confidence) ───────── */
.result-stat-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-bottom: 0.3rem;
}
.result-stat-value {
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}
.result-prob-box {
    background: var(--purple-dim);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: var(--radius);
    padding: 1rem 1.25rem 0.25rem 1.25rem;
    margin-top: 1.25rem;
}

/* ── Result Container ────────────────────────────────── */
.result-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem;
    margin: 1rem 0;
    position: relative;
}

/* ── Info Card ───────────────────────────────────────── */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin: 0.5rem 0;
}
.info-card-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.info-card-value {
    font-size: 0.95rem;
    color: var(--text-primary);
    font-weight: 500;
}

/* ── Architecture Block ──────────────────────────────── */
.arch-block {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.8;
    white-space: pre;
    overflow-x: auto;
}
.arch-highlight { color: var(--purple-light); font-weight: 600; }

/* ── Tag / Pill ──────────────────────────────────────── */
.tag {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.tag-purple { background: var(--purple-dim); color: var(--purple-light); }
.tag-green  { background: var(--green-dim);  color: var(--green);  }
.tag-red    { background: var(--red-dim);    color: var(--red);    }
.tag-amber  { background: var(--amber-dim);  color: var(--amber);  }

/* ── Divider ─────────────────────────────────────────── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}

/* ── Hero Banner ─────────────────────────────────────── */
.hero-banner {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--purple);
    border-radius: var(--radius);
    padding: 2rem;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.3;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    max-width: 600px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--purple-dim);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 100px;
    padding: 0.3rem 0.8rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--purple-light);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
}

/* ── Per-class F1 Row ────────────────────────────────── */
.f1-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border);
}
.f1-row:last-child { border-bottom: none; }
.f1-class { font-size: 0.85rem; font-weight: 500; color: var(--text-primary); }
.f1-bar-wrap { flex: 1; margin: 0 1rem; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.f1-bar { height: 100%; border-radius: 3px; }
.f1-score { font-size: 0.85rem; font-weight: 700; font-family: var(--font-mono); color: var(--text-primary); min-width: 3rem; text-align: right; }

/* ── Streamlit component overrides ──────────────────── */
.stTextArea textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-main) !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--purple) !important;
    box-shadow: 0 0 0 2px var(--purple-dim) !important;
}
.stButton > button {
    background: var(--purple) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: var(--font-main) !important;
    padding: 0.6rem 1.5rem !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: var(--purple-light) !important;
}
.stSelectbox [data-baseweb="select"] {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.25rem !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--purple-light) !important;
    border-bottom-color: var(--purple) !important;
    background: transparent !important;
}
.stFileUploader {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--purple), var(--purple-light)) !important;
}
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: none !important;
}
</style>
"""


def inject_css():
    """Inject CSS global ke halaman Streamlit."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def section_header(title: str, icon: str = ""):
    """Render section header dengan garis aksen kiri."""
    import streamlit as st
    label = f"{icon} {title}" if icon else title
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-dot"></div>
            <div class="section-title">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result: dict):
    """Render kartu hasil prediksi sentimen dengan breakdown probabilitas per kelas."""
    import streamlit as st

    label      = result["label"]
    confidence = result["confidence"]
    probs      = result["probs"]

    emoji_map    = {"positive": "😊", "negative": "😞", "neutral": "😐"}
    label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
    colors       = {"positive": "#10B981", "negative": "#EF4444", "neutral": "#F59E0B"}

    # HTML dibangun flush-left tanpa indentasi/baris kosong — markdown parser
    # Streamlit bisa salah mengartikan HTML berindentasi sebagai code block,
    # yang menyebabkan tag penutup seperti "</div>" malah ter-render sebagai teks.
    rows = "".join(
        f'<div class="f1-row">'
        f'<span class="f1-class">{emoji_map[key]} {label_id_map[key]}</span>'
        f'<div class="f1-bar-wrap"><div class="f1-bar" style="width:{prob*100:.1f}%; background:{colors[key]};"></div></div>'
        f'<span class="f1-score" style="color:{colors[key]};">{prob*100:.1f}%</span>'
        f'</div>'
        for key, prob in zip(["positive", "negative", "neutral"], probs)
    )

    html = (
        f'<div class="result-container {label}">'
        f'<div style="display:flex; gap:2rem; margin-bottom:0.5rem;">'
        f'<div style="flex:1;">'
        f'<div class="result-stat-label">Kategori Sentimen</div>'
        f'<div class="result-stat-value" style="color:{colors[label]};">{label_id_map[label]} {emoji_map[label]}</div>'
        f'</div>'
        f'<div style="flex:1;">'
        f'<div class="result-stat-label">Confidence Score</div>'
        f'<div class="result-stat-value">{confidence*100:.1f}%</div>'
        f'</div>'
        f'</div>'
        f'<div class="result-prob-box">{rows}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
