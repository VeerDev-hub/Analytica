import io
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


def setup_page_config():
    st.set_page_config(
        page_title="Analytica Studio",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_global_theme():
    css = """
        <style>
        :root {{
            color-scheme: light dark;
            --app-bg: radial-gradient(circle at top, #fbfdff 0%, #f4f7fb 45%, #e9eef5 100%);
            --surface: rgba(255, 255, 255, 0.92);
            --surface-soft: rgba(248, 250, 252, 0.96);
            --border: rgba(15, 23, 42, 0.10);
            --text-main: #0f172a;
            --text-muted: #475569;
            --accent: #2563eb;
            --accent-soft: rgba(37, 99, 235, 0.14);
            --shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
            --sidebar-bg: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(241,245,249,0.96));
            --menu-bg: #ffffff;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                color-scheme: dark;
                --app-bg: radial-gradient(circle at top, #172554 0%, #0f172a 42%, #020617 100%);
                --surface: rgba(15, 23, 42, 0.82);
                --surface-soft: rgba(30, 41, 59, 0.78);
                --border: rgba(148, 163, 184, 0.16);
                --text-main: #e2e8f0;
                --text-muted: #94a3b8;
                --accent: #60a5fa;
                --accent-soft: rgba(96, 165, 250, 0.16);
                --shadow: 0 20px 60px rgba(2, 6, 23, 0.45);
                --sidebar-bg: linear-gradient(180deg, rgba(15,23,42,0.97), rgba(2,6,23,0.97));
                --menu-bg: #0f172a;
            }}
        }}

        html, body, [class*="css"] {{
            color: var(--text-main);
            font-family: "Trebuchet MS", "Segoe UI", sans-serif;
            background-color: var(--app-bg);
        }}

        .stApp {{
            background: var(--app-bg);
            color: var(--text-main);
        }}

        .block-container {{
            max-width: 1380px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-bottom: 3rem;
            padding-left: 2rem;
        }}

        [data-testid="stSidebar"] {{
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--text-main);
        }}

        h1, h2, h3, h4, h5, h6, p, label, span, div, li {{
            color: var(--text-main);
        }}

        [data-testid="stCaptionContainer"] p,
        .stCaption,
        .stMarkdown p {{
            color: var(--text-muted);
        }}

        div[data-testid="metric-container"],
        .stDataFrame,
        .stAlert,
        .stTabs [data-baseweb="tab-panel"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            border-radius: 18px;
            backdrop-filter: blur(14px);
        }}

        div[data-testid="metric-container"] {{
            padding: 1rem 1rem 0.9rem;
            margin-bottom: 0.75rem;
        }}

        .stMarkdown,
        .stDataFrame,
        .stAlert,
        .stTabs,
        .stPlotlyChart,
        .stDownloadButton,
        .stButton,
        .stSelectbox,
        .stMultiSelect,
        .stSlider,
        .stRadio,
        .stCheckbox {{
            margin-bottom: 0.8rem;
        }}

        div[data-testid="stHorizontalBlock"] > div {{
            gap: 1rem;
        }}

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stFileUploader label,
        .stSelectbox label,
        .stMultiSelect label,
        .stRadio label,
        .stCheckbox label,
        .stSlider label,
        .stDownloadButton label,
        .stButton label {{
            color: var(--text-main) !important;
        }}

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        [data-baseweb="select"] > div,
        [data-baseweb="base-input"] > div,
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] {{
            background: var(--surface-soft) !important;
            color: var(--text-main) !important;
            border-color: var(--border) !important;
        }}

        [data-baseweb="select"] input {{
            color: var(--text-main) !important;
        }}

        [role="listbox"],
        [data-baseweb="menu"],
        [data-baseweb="popover"] {{
            background: var(--menu-bg) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
        }}

        [role="option"] {{
            background: transparent !important;
            color: var(--text-main) !important;
        }}

        [role="option"]:hover {{
            background: rgba(96, 165, 250, 0.14) !important;
        }}

        .stCheckbox div[data-testid="stMarkdownContainer"] p,
        .stRadio div[data-testid="stMarkdownContainer"] p,
        .stSelectbox div[data-testid="stMarkdownContainer"] p,
        .stMultiSelect div[data-testid="stMarkdownContainer"] p,
        .stSlider div[data-testid="stMarkdownContainer"] p {{
            color: var(--text-main) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            margin-bottom: 0.8rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 999px;
            padding: 0.45rem 0.95rem;
            background: var(--surface-soft) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, var(--accent), #38bdf8) !important;
            color: #f8fafc !important;
            border-color: transparent !important;
        }}

        .stTabs [data-baseweb="tab"] p {{
            color: inherit !important;
        }}

        .stDownloadButton button,
        .stButton button {{
            background: linear-gradient(135deg, var(--accent), #38bdf8);
            color: #f8fafc;
            border: none;
            border-radius: 14px;
            padding: 0.65rem 1.25rem;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.20);
        }}

        .stDownloadButton button:hover,
        .stButton button:hover {{
            filter: brightness(1.03);
        }}

        section[data-testid="stFileUploader"] {{
            background: var(--surface-soft);
            border: 1px dashed var(--accent);
            border-radius: 18px;
            padding: 0.8rem;
        }}

        [data-testid="stFileUploaderDropzone"] * {{
            color: var(--text-main) !important;
        }}

        [data-testid="stDataFrame"] *,
        .stDataFrame * {{
            color: var(--text-main) !important;
        }}

        table, thead, tbody, tr, th, td {{
            color: var(--text-main) !important;
            background-color: transparent !important;
        }}

        .stAlert * {{
            color: var(--text-main) !important;
        }}

        hr {{
            border-color: var(--border);
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-top: 1.25rem;
                padding-right: 1rem;
                padding-bottom: 2rem;
                padding-left: 1rem;
            }}
        }}
        </style>
        """.format(
    )
    st.markdown(
        css,
        unsafe_allow_html=True,
    )


def show_header():
    st.caption("Data workspace")
    st.title("Analytica Studio")
    st.write("Fast local data analysis with cleaner visuals and better readability across themes.")
    col1, col2, col3 = st.columns(3)
    col1.caption("CSV and Excel support")
    col2.caption("Local-first processing")
    col3.caption("Interactive analysis")
    st.divider()


def show_footer():
    st.divider()
    st.caption("Analytica Studio | Automated data analysis workspace | Built by Veer")


def show_empty_state():
    st.info("Upload a CSV or Excel dataset to begin. Processing stays local and works across desktop and mobile.")


def display_metrics_row(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", f"{df.shape[0]:,}")
    col2.metric("Total Columns", f"{df.shape[1]}")
    col3.metric("Numeric Columns", df.select_dtypes(include=[np.number]).shape[1])
    col4.metric("Categorical Columns", df.select_dtypes(include=["object"]).shape[1])


def display_quality_metrics(df):
    col1, col2, col3 = st.columns(3)
    missing = df.isna().sum().sum()
    missing_pct = (missing / (df.shape[0] * df.shape[1]) * 100)
    col1.metric("Missing Values", f"{missing:,}", f"{missing_pct:.2f}%")
    col2.metric("Duplicate Rows", f"{df.duplicated().sum():,}")
    memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    col3.metric("Memory Usage", f"{memory:.2f} MB")


def display_data_preview(df, rows=10):
    st.markdown("## Data Preview")
    st.dataframe(df.head(rows), use_container_width=True)


def export_as_csv(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    st.download_button("Download CSV", df.to_csv(index=False), filename, "text/csv")


def export_as_excel(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        "Download Excel",
        buffer.getvalue(),
        filename,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def display_quality_assessment(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    duplicate_pct = (df.duplicated().sum() / len(df) * 100)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Data Completeness")
        st.metric("Completeness Score", f"{completeness:.1f}%")
        st.success("Excellent quality" if completeness >= 95 else "Needs attention")

    with col2:
        st.markdown("## Uniqueness")
        st.metric("Unique Rows", f"{(100 - duplicate_pct):.1f}%")


def display_column_stats(df, selected_col):
    series = df[selected_col].dropna()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean", f"{series.mean():.4f}")
    col2.metric("Median", f"{series.median():.4f}")
    col3.metric("Std Dev", f"{series.std():.4f}")
    col4.metric("Range", f"{series.max() - series.min():.4f}")


def display_insights_cards(insights):
    c1, c2 = st.columns(2)

    if "most_varied_column" in insights:
        c1.info(f"Most varied column: {insights['most_varied_column']['column']}")

    if "most_correlated_pair" in insights:
        pair = insights["most_correlated_pair"]
        c2.info(
            f"Highest correlation: {pair['columns'][0]} and {pair['columns'][1]} ({pair['correlation']:.3f})"
        )


def sidebar_file_uploader():
    with st.sidebar:
        st.subheader("Upload Data")
        return st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])


def sidebar_file_info(uploaded_file, df):
    with st.sidebar:
        st.success(f"Loaded: {uploaded_file.name}")
        st.caption(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")


def display_data_summary(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100

    st.markdown("## File Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]}")
    col3.metric("Memory (MB)", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f}")
    col4.metric("Completeness", f"{completeness:.1f}%")

    st.markdown("### Column Types")
    t1, t2, t3 = st.columns(3)
    t1.metric("Numeric", df.select_dtypes(include=[np.number]).shape[1])
    t2.metric("Text", df.select_dtypes(include=["object"]).shape[1])
    t3.metric("Other", df.select_dtypes(exclude=[np.number, "object"]).shape[1])


def sidebar_navigation():
    with st.sidebar:
        st.markdown("---")
        st.subheader("Analytica")
        st.caption("Data intelligence console")
        return option_menu(
            None,
            ["Overview", "Statistics", "Visualizations", "Insights", "Preprocessing", "Export"],
            icons=["house", "calculator", "bar-chart", "lightbulb", "sliders", "download"],
            styles={
                "container": {"background-color": "transparent", "padding": "0"},
                "icon": {"color": "var(--accent)"},
                "nav-link": {
                    "color": "var(--text-main)",
                    "margin": "6px 0",
                    "border-radius": "12px",
                    "background-color": "var(--surface-soft)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(251, 146, 60, 0.18), rgba(245, 158, 11, 0.26))",
                    "font-weight": "700",
                    "color": "#f59e0b",
                    "border": "1px solid rgba(245, 158, 11, 0.38)",
                    "box-shadow": "0 0 0 1px rgba(245, 158, 11, 0.12) inset",
                },
            },
        )
