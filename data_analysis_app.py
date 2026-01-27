import streamlit as st
from ui_components import (
    setup_page_config, setup_custom_styling, show_header, show_footer,
    sidebar_file_uploader, sidebar_file_info, sidebar_navigation
)
from preprocessing import load_and_clean_data
from pages import (
    page_overview, page_statistics, page_visualizations,
    page_insights, page_preprocessing, page_export
)
import pandas as pd

# Page setup
setup_page_config()
setup_custom_styling()
show_header()

# Initialize session state
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None


def load_data(uploaded_file):
    """Loads data from uploaded file without cleaning."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Sidebar
uploaded_file = sidebar_file_uploader()

if uploaded_file is None:
    st.info("👈 Upload a file to get started!")
else:
    # Check if it's a new file
    if st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.uploaded_file_name = uploaded_file.name
        df_raw = load_data(uploaded_file)
        if df_raw is not None:
            st.session_state.df_raw = df_raw
            st.session_state.df_processed = df_raw.copy() # Start with a copy

    if st.session_state.df_processed is not None:
        sidebar_file_info(uploaded_file, st.session_state.df_processed)

        # Main navigation
        page = sidebar_navigation()

        # Page content
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