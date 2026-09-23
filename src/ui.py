"""Shared CSS and reusable Streamlit UI helpers for a modern dashboard look."""

# Professional palette (no purple/indigo)
PRIMARY = "#2563EB"       # blue-600
PRIMARY_DARK = "#1E40AF"  # blue-800
ACCENT = "#0EA5E9"        # sky-500
SUCCESS = "#16A34A"       # green-600
WARNING = "#F59E0B"        # amber-500
DANGER = "#DC2626"        # red-600
BG = "#0F172A"            # slate-900
CARD_BG = "#1E293B"       # slate-800
TEXT = "#F1F5F9"          # slate-100
MUTED = "#94A3B8"         # slate-400

CSS = """
<style>
    /* Global */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
        color: #F1F5F9;
    }
    .stApp h1, .stApp h2, .stApp h3 { color: #F1F5F9 !important; font-weight: 700; }
    .stApp p, .stApp span, .stApp li { color: #CBD5E1; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0B1220;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2 { color: #60A5FA !important; }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #172033 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(37,99,235,0.25); }
    .kpi-icon { font-size: 26px; margin-bottom: 6px; }
    .kpi-label { color: #94A3B8; font-size: 13px; text-transform: uppercase; letter-spacing: .5px; }
    .kpi-value { color: #F1F5F9; font-size: 30px; font-weight: 800; margin-top: 2px; }
    .kpi-sub { color: #64748B; font-size: 12px; margin-top: 4px; }

    /* Section headers */
    .section-title {
        font-size: 22px; font-weight: 700; color: #F1F5F9;
        border-left: 4px solid #2563EB; padding-left: 12px; margin: 8px 0 4px 0;
    }
    .section-sub { color: #94A3B8; font-size: 14px; margin-bottom: 16px; }

    /* Insight callouts */
    .insight-box {
        background: #16203300; border: 1px solid #1E3A5F; border-radius: 12px;
        padding: 14px 18px; margin: 10px 0;
    }
    .insight-box .insight-tag {
        display: inline-block; background: #2563EB; color: #fff; font-size: 11px;
        font-weight: 700; padding: 2px 10px; border-radius: 999px; margin-bottom: 6px;
    }
    .insight-box .insight-text { color: #CBD5E1; font-size: 14px; }

    /* Risk gauge */
    .risk-card {
        border-radius: 16px; padding: 24px; text-align: center;
        border: 1px solid #334155; background: #1E293B;
    }
    .risk-prob { font-size: 42px; font-weight: 800; }
    .risk-label { font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    /* Tables */
    .stDataFrame, .stTable { border-radius: 12px; overflow: hidden; }

    /* Metric tiles */
    [data-testid="stMetric"] {
        background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 12px 16px;
    }
    [data-testid="stMetricValue"] { color: #F1F5F9 !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: #fff; border: none; border-radius: 10px; font-weight: 600;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); }

    /* Select boxes / inputs */
    .stSelectbox > div > div, .stNumberInput input, .stTextInput input {
        background: #0F172A !important; color: #F1F5F9 !important; border-color: #334155 !important;
    }

    /* Footer */
    .footer { color: #64748B; font-size: 12px; text-align: center; margin-top: 32px; padding-top: 16px; border-top: 1px solid #1E293B; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def kpi_card(icon, label, value, sub=""):
    import streamlit as st
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {f'<div class="kpi-sub">{sub}</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)


def section_header(title, subtitle=""):
    import streamlit as st
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def insight_box(tag, text):
    import streamlit as st
    st.markdown(f"""
    <div class="insight-box">
        <span class="insight-tag">{tag}</span>
        <div class="insight-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)
