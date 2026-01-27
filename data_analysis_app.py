import streamlit as st
import pandas as pd

from ui_components import (
    setup_page_config,
    apply_global_theme,
    show_header,
    show_footer,
    sidebar_file_uploader,
    sidebar_file_info,
    sidebar_navigation
)

from preprocessing import load_and_clean_data
from pages import (
    page_overview,
    page_statistics,
    page_visualizations,
    page_insights,
    page_preprocessing,
    page_export
)


setup_page_config()
apply_global_theme()
show_header()


if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None

if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None

if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None



def load_data(uploaded_file):
    try:
        with st.spinner("📊 Loading dataset..."):
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.toast("Dataset loaded successfully 🚀")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None



uploaded_file = sidebar_file_uploader()

if uploaded_file is None:
    st.markdown("""
    <div style="margin-top:6rem; text-align:center;">
        <h2>📁 Upload a dataset to begin</h2>
        <p style="color:#94a3b8;">
        Supports CSV and Excel files • Max 100MB • Local processing
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # New file uploaded
    if st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.uploaded_file_name = uploaded_file.name
        df_raw = load_data(uploaded_file)

        if df_raw is not None:
            st.session_state.df_raw = df_raw
            st.session_state.df_processed = df_raw.copy()

    if st.session_state.df_processed is not None:

        sidebar_file_info(uploaded_file, st.session_state.df_processed)

        # Navigation
        page = sidebar_navigation()



        if page == "Overview":
            page_overview(st.session_state.df_processed)

        elif page == "Statistics":
            page_statistics(st.session_state.df_processed)

        elif page == "Visualizations":
            page_visualizations(st.session_state.df_processed)

        elif page == "Insights":
            page_insights(st.session_state.df_processed)

        elif page == "Preprocessing":
            page_preprocessing()

        elif page == "Export":
            page_export(st.session_state.df_processed)



show_footer()
