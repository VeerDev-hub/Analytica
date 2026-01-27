import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from datetime import datetime
import io


def setup_page_config():
    st.set_page_config(
        page_title="Analytica Studio",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def setup_custom_styling():
    st.markdown("""
    <style>
        .main {
            padding: 0rem 0rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)


def show_header():
    st.markdown("#Analytica Studio")
    st.markdown("Fast local data analysis with instant results")


def show_footer():
    st.markdown("""
    <hr>
    <p style="text-align:center; color:gray;">
    Analytica • Automated Data Analysis Studio • Made with love by Veer
    </p>
    """, unsafe_allow_html=True)


def display_metrics_row(df):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Total Columns", f"{df.shape[1]}")
    with col3:
        numeric = df.select_dtypes(include=[np.number]).shape[1]
        st.metric("Numeric Cols", numeric)
    with col4:
        categorical = df.select_dtypes(include=['object']).shape[1]
        st.metric("Categorical Cols", categorical)


def display_quality_metrics(df):
    col1, col2, col3 = st.columns(3)
    with col1:
        missing = df.isna().sum().sum()
        missing_pct = (missing / (df.shape[0] * df.shape[1]) * 100)
        st.metric("Missing Values", f"{missing:,}", f"{missing_pct:.2f}%")
    with col2:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", f"{duplicates:,}")
    with col3:
        memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Memory Usage", f"{memory:.2f} MB")


def display_data_preview(df, rows=10):
    st.markdown("### Data Preview")
    st.dataframe(df.head(rows), use_container_width=True)


def export_as_csv(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


def export_as_excel(df, filename=None):
    if filename is None:
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        label="📥 Download as Excel",
        data=excel_buffer.getvalue(),
        file_name=filename,
        mime="application/vnd.ms-excel"
    )


def display_data_summary(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    summary_text = f"""
**File Summary**
- Rows: {df.shape[0]:,}
- Columns: {df.shape[1]}
- Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
- Complete: {completeness:.1f}%

**Column Types**
- Numeric: {df.select_dtypes(include=[np.number]).shape[1]}
- Text: {df.select_dtypes(include=['object']).shape[1]}
- Other: {df.select_dtypes(exclude=[np.number, 'object']).shape[1]}
"""
    st.markdown(summary_text)


def display_quality_assessment(df):
    completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    duplicate_pct = (df.duplicated().sum() / len(df) * 100)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Data Completeness")
        st.metric("Completeness Score", f"{completeness:.1f}%")
        if completeness >= 95:
            st.success("✅ Excellent data quality")
        elif completeness >= 80:
            st.warning("⚠️ Some missing values")
        else:
            st.error("❌ Many missing values")
    with col2:
        st.markdown("### Uniqueness")
        st.metric("Unique Rows", f"{(100-duplicate_pct):.1f}%")
        if duplicate_pct == 0:
            st.success("✅ No duplicates found")
        elif duplicate_pct < 5:
            st.warning(f"⚠️ {duplicate_pct:.2f}% duplicates")
        else:
            st.error(f"❌ {duplicate_pct:.2f}% duplicates")


def display_column_stats(df, selected_col):
    series = df[selected_col].dropna()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean", f"{series.mean():.4f}")
    with col2:
        st.metric("Median", f"{series.median():.4f}")
    with col3:
        st.metric("Std Dev", f"{series.std():.4f}")
    with col4:
        st.metric("Range", f"{series.max() - series.min():.4f}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Min Value", f"{series.min():.4f}")
    with col2:
        st.metric("Max Value", f"{series.max():.4f}")


def display_insights_cards(insights):
    insights_col1, insights_col2 = st.columns(2)
    with insights_col1:
        if 'most_varied_column' in insights:
            col_name = insights['most_varied_column']['column']
            std_val = insights['most_varied_column']['std_dev']
            st.markdown("**Most Varied Column**")
            st.info(f"{col_name}: σ = {std_val:.4f}")
        if 'least_varied_column' in insights:
            col_name = insights['least_varied_column']['column']
            std_val = insights['least_varied_column']['std_dev']
            st.markdown("**Least Varied Column**")
            st.info(f"{col_name}: σ = {std_val:.4f}")
    with insights_col2:
        if 'most_correlated_pair' in insights:
            pair = insights['most_correlated_pair']['columns']
            corr = insights['most_correlated_pair']['correlation']
            st.markdown("**Most Correlated Pair**")
            st.info(f"{pair[0]} ↔ {pair[1]}: {corr:.4f}")

def sidebar_file_uploader():
    """Renders the file uploader in the sidebar."""
    with st.sidebar:
        st.markdown("## 📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Max 100MB"
        )
    return uploaded_file

def sidebar_file_info(uploaded_file, df):
    """Displays file info in the sidebar."""
    with st.sidebar:
        st.success(f"✅ Loaded: {uploaded_file.name}")
        st.markdown(f"**Rows:** {df.shape[0]:,} | **Columns:** {df.shape[1]}")

def sidebar_navigation():
    with st.sidebar:

        st.markdown("""
        <style>
        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #020617);
        }

        /* Remove default padding */
        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("##Analytica Studio")
        st.markdown("<p style='color:#94a3b8'>Data Intelligence Console</p>", unsafe_allow_html=True)
        st.markdown("---")

        page = option_menu(
            menu_title=None,
            options=["Overview", "Statistics", "Visualizations", "Insights", "Preprocessing", "Export"],
            icons=["house", "calculator", "bar-chart", "lightbulb", "gear", "download"],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#38bdf8",
                    "font-size": "20px"
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "6px",
                    "color": "#e5e7eb",
                    "border-radius": "10px",
                    "padding": "10px"
                },
                "nav-link:hover": {
                    "background-color": "#1e293b"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #2563eb, #38bdf8)",
                    "color": "white",
                    "font-weight": "600",
                    "border-radius": "12px",
                    "box-shadow": "0 4px 12px rgba(56,189,248,0.4)"
                }
            }
        )

    return page
