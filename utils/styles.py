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
    --radius:         12px;
    --radius-sm:      8px;
    --shadow:         0 4px 24px rgba(0,0,0,0.4);
    --shadow-glow:    0 0 32px rgba(108, 99, 255, 0.2);
}

/* ── Base Reset ──────────────────────────────────────── */
*, html, body {
    font-family: var(--font-main) !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
}

/* ── Hide Streamlit default branding ────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

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
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--purple), var(--purple-light));
}
.metric-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow-glow);
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

/* ── Result Badge ────────────────────────────────────── */
.result-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.25rem;
    border-radius: 100px;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 0.02em;
}
.badge-positive { background: var(--green-dim); color: var(--green); border: 1px solid var(--green); }
.badge-negative { background: var(--red-dim);   color: var(--red);   border: 1px solid var(--red);   }
.badge-neutral  { background: var(--amber-dim); color: var(--amber); border: 1px solid var(--amber); }

/* ── Result Container ────────────────────────────────── */
.result-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem;
    margin: 1rem 0;
    position: relative;
}
.result-container.positive { border-left: 3px solid var(--green); }
.result-container.negative { border-left: 3px solid var(--red);   }
.result-container.neutral  { border-left: 3px solid var(--amber); }

.confidence-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}
.confidence-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
}
.confidence-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    font-family: var(--font-mono);
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
    background: linear-gradient(135deg, #141627 0%, #1a1040 50%, #0f1628 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
    pointer-events: none;
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
    background: linear-gradient(135deg, var(--purple), #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: var(--font-main) !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s, box-shadow 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    box-shadow: 0 4px 16px rgba(108,99,255,0.4) !important;
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


def render_result_card(result: dict, text: str = ""):
    """Render kartu hasil prediksi sentimen."""
    import streamlit as st

    label      = result["label"]
    confidence = result["confidence"]
    probs      = result["probs"]

    emoji_map = {"positive": "😊", "negative": "😞", "neutral": "😐"}
    label_id_map = {"positive": "Positif", "negative": "Negatif", "neutral": "Netral"}
    emoji  = emoji_map[label]
    label_id = label_id_map[label]

    st.markdown(
        f"""
        <div class="result-container {label}">
            <div style="margin-bottom:1rem;">
                <span class="result-badge badge-{label}">{emoji} {label_id}</span>
            </div>
            <div class="confidence-row">
                <span class="confidence-label">Confidence</span>
                <span class="confidence-value">{confidence*100:.1f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Probability bar chart via Plotly
    import plotly.graph_objects as go
    label_names = ["Positif", "Negatif", "Netral"]
    colors      = ["#10B981", "#EF4444", "#F59E0B"]
    fig = go.Figure(go.Bar(
        x=label_names,
        y=[p * 100 for p in probs],
        marker_color=colors,
        marker_line_width=0,
        text=[f"{p*100:.1f}%" for p in probs],
        textposition="outside",
        textfont=dict(color="#E8E9F3", size=12, family="JetBrains Mono"),
    ))
    fig.update_layout(
        plot_bgcolor="#141627",
        paper_bgcolor="#141627",
        font=dict(color="#9899B0", family="Inter"),
        yaxis=dict(
            range=[0, 110], showgrid=True,
            gridcolor="#252842", gridwidth=1,
            ticksuffix="%", tickfont=dict(size=11),
        ),
        xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#E8E9F3")),
        margin=dict(t=20, b=10, l=10, r=10),
        height=240,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
