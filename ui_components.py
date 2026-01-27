import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from datetime import datetime
import io


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

def setup_page_config():
    st.set_page_config(
        page_title="Analytica Studio",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_global_theme():
    st.markdown("""
    <style>

    /* App background */
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617 70%);
        color: #e5e7eb;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Remove top whitespace */
    .block-container {
        padding-top: 2rem;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc;
        letter-spacing: 0.4px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #020617, #0f172a);
        border: 1px solid rgba(148,163,184,0.15);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.15);
    }

    /* Buttons */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2563eb, #38bdf8);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stDownloadButton button:hover {
        transform: scale(1.04);
        box-shadow: 0 6px 22px rgba(56,189,248,0.4);
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        background: #020617;
        border: 1px dashed #38bdf8;
        border-radius: 16px;
        padding: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# HEADER & FOOTER
# --------------------------------------------------

def show_header():
    st.markdown("""
    <h1 style="font-size:3rem;">📊 Analytica Studio</h1>
    <p style="color:#94a3b8; font-size:1.1rem;">
    Fast • Local • Intelligent Data Analysis Console
    </p>
    <hr style="margin-top:1rem; margin-bottom:2rem; border-color:#1e293b;">
    """, unsafe_allow_html=True)


def show_footer():
    st.markdown("""
    <hr style="margin-top:3rem; border-color:#1e293b;">
    <p style="text-align:center; color:#94a3b8;">
    Analytica • Automated Data Analysis Studio • Built by Veer
    </p>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# DATA OVERVIEW
# --------------------------------------------------

def display_metrics_row(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", f"{df.shape[0]:,}")
    col2.metric("Total Columns", f"{df.shape[1]}")
    col3.metric("Numeric Columns", df.select_dtypes(include=[np.number]).shape[1])
    col4.metric("Categorical Columns", df.select_dtypes(include=['object']).shape[1])


def display_quality_metrics(df):
    col1, col2, col3 = st.columns(3)
    missing = df.isna().sum().sum()
    missing_pct = (missing / (df.shape[0] * df.shape[1]) * 100)
    col1.metric("Missing Values", f"{missing:,}", f"{missing_pct:.2f}%")
    col2.metric("Duplicate Rows", f"{df.duplicated().sum():,}")
    memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    col3.metric("Memory Usage", f"{memory:.2f} MB")


def display_data_preview(df, rows=10):
    st.markdown("## 🔍 Data Preview")
    st.dataframe(df.head(rows), use_container_width=True)


# --------------------------------------------------
# EXPORT
# --------------------------------------------------

def export_as_csv(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    st.download_button("📥 Download as CSV", df.to_csv(index=False), filename, "text/csv")


def export_as_excel(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button("📥 Download as Excel", buffer.getvalue(), filename,
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# --------------------------------------------------
# QUALITY & INSIGHTS
# --------------------------------------------------

def display_quality_assessment(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    duplicate_pct = (df.duplicated().sum() / len(df) * 100)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## 📊 Data Completeness")
        st.metric("Completeness Score", f"{completeness:.1f}%")
        st.success("Excellent quality" if completeness >= 95 else "Needs attention")

    with col2:
        st.markdown("## 🧬 Uniqueness")
        st.metric("Unique Rows", f"{(100-duplicate_pct):.1f}%")


def display_column_stats(df, selected_col):
    series = df[selected_col].dropna()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean", f"{series.mean():.4f}")
    col2.metric("Median", f"{series.median():.4f}")
    col3.metric("Std Dev", f"{series.std():.4f}")
    col4.metric("Range", f"{series.max() - series.min():.4f}")


def display_insights_cards(insights):
    c1, c2 = st.columns(2)

    if 'most_varied_column' in insights:
        c1.info(f"📈 Most Varied: {insights['most_varied_column']['column']}")

    if 'most_correlated_pair' in insights:
        p = insights['most_correlated_pair']
        c2.info(f"🔗 Highest Correlation: {p['columns'][0]} ↔ {p['columns'][1]} ({p['correlation']:.3f})")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

def sidebar_file_uploader():
    with st.sidebar:
        st.markdown("## 📁 Upload Data")
        return st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx', 'xls'])


def sidebar_file_info(uploaded_file, df):
    with st.sidebar:
        st.success(f"Loaded: {uploaded_file.name}")
        st.markdown(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")




def display_data_summary(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100

    st.markdown("## 📄 File Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]}")
    col3.metric("Memory (MB)", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f}")
    col4.metric("Completeness", f"{completeness:.1f}%")

    st.markdown("### Column Types")

    t1, t2, t3 = st.columns(3)
    t1.metric("Numeric", df.select_dtypes(include=[np.number]).shape[1])
    t2.metric("Text", df.select_dtypes(include=['object']).shape[1])
    t3.metric("Other", df.select_dtypes(exclude=[np.number, 'object']).shape[1])


def sidebar_navigation():
    with st.sidebar:

        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #020617);
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <h2 style="margin-bottom:0;">📊 Analytica</h2>
        <p style="color:#94a3b8; font-size:0.85rem;">Data Intelligence Console</p>
        <hr>
        """, unsafe_allow_html=True)

        return option_menu(
            None,
            ["Overview", "Statistics", "Visualizations", "Insights", "Preprocessing", "Export"],
            icons=["house", "calculator", "bar-chart", "lightbulb", "gear", "download"],
            styles={
                "container": {"background-color": "transparent"},
                "icon": {"color": "#38bdf8"},
                "nav-link": {"color": "#e5e7eb", "margin": "6px", "border-radius": "10px"},
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #2563eb, #38bdf8)",
                    "font-weight": "600"
                }
            }
        )
