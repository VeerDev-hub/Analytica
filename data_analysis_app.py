import streamlit as st

from pages import (
    page_export,
    page_insights,
    page_overview,
    page_preprocessing,
    page_statistics,
    page_visualizations,
)
from preprocessing import load_and_clean_data_from_bytes
from ui_components import (
    setup_page_config,
    apply_global_theme,
    show_empty_state,
    show_footer,
    show_header,
    sidebar_file_info,
    sidebar_file_uploader,
    sidebar_navigation,
)


setup_page_config()


if "df_raw" not in st.session_state:
    st.session_state.df_raw = None

if "df_processed" not in st.session_state:
    st.session_state.df_processed = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

apply_global_theme()
show_header()


@st.cache_data(show_spinner=False)
def load_data_cached(file_bytes, file_name):
    return load_and_clean_data_from_bytes(file_bytes, file_name)


def load_data(uploaded_file):
    try:
        with st.spinner("Loading dataset..."):
            file_bytes = uploaded_file.getvalue()
            df = load_data_cached(file_bytes, uploaded_file.name)
        st.toast("Dataset loaded successfully")
        return df
    except Exception as exc:
        st.error(f"Error loading file: {exc}")
        return None


uploaded_file = sidebar_file_uploader()

if uploaded_file is None:
    show_empty_state()
else:
    if st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.uploaded_file_name = uploaded_file.name
        df_raw = load_data(uploaded_file)

        if df_raw is not None:
            st.session_state.df_raw = df_raw
            st.session_state.df_processed = df_raw.copy()

    if st.session_state.df_processed is not None:
        sidebar_file_info(uploaded_file, st.session_state.df_processed)
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
