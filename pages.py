import streamlit as st
import pandas as pd
import numpy as np
from analytics import (
    get_column_info, calculate_stats, get_missing_data_analysis,
    get_data_quality_metrics, get_summary_statistics, get_statistical_insights
)
from visualizations import (
    create_histogram, create_correlation_heatmap, create_box_plot,
    create_scatter_plot, create_data_heatmap
)
from ui_components import (
    display_metrics_row, display_quality_metrics, display_data_preview,
    export_as_csv, export_as_excel, display_data_summary,
    display_quality_assessment, display_column_stats, display_insights_cards
)
from preprocessing import (
    handle_missing_values, remove_duplicates, remove_outliers, scale_features, clean_data
)


def page_overview(df):
    st.markdown("## 📊 Data Overview")
    display_metrics_row(df)
    display_data_preview(df)
    st.markdown("### Column Information")
    col_info = get_column_info(df)
    st.dataframe(col_info, use_container_width=True)
    st.markdown("### Data Quality")
    display_quality_metrics(df)


def page_statistics(df):
    st.markdown("## 🔢 Descriptive Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        st.error("❌ No numeric columns detected!")
        st.markdown("### Debug Info:")
        col_info = get_column_info(df)
        st.dataframe(col_info, use_container_width=True)
        st.markdown("### Tips to fix:")
        st.markdown("""
        - Check that numeric columns don't have letters or symbols
        - Try removing currency symbols ($, €, etc)
        - Try removing thousand separators (,)
        - Check for extra spaces or special characters
        - Ensure numbers aren't in quote marks
        """)
        return
    stats_df = calculate_stats(df)
    st.dataframe(stats_df, use_container_width=True)
    st.markdown("### Deep Dive into Column")
    selected_col = st.selectbox("Select column", numeric_cols)
    display_column_stats(df, selected_col)
    st.markdown("### Missing Data")
    missing_df = get_missing_data_analysis(df)
    if len(missing_df) > 0:
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("✅ No missing values detected!")


def page_visualizations(df):
    st.markdown("## 📈 Data Visualizations")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Distributions", "Correlations", "Box Plots", "Scatter", "Heatmap"
    ])
    with tab1:
        st.markdown("### Distribution Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="dist_col")
            fig = create_histogram(df, col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available")
    with tab2:
        st.markdown("### Correlation Analysis")
        if len(numeric_cols) > 1:
            fig = create_correlation_heatmap(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns")
    with tab3:
        st.markdown("### Box Plot Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="box_col")
            fig = create_box_plot(df, col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available")
    with tab4:
        st.markdown("### Scatter Plot")
        if len(numeric_cols) > 1:
            col1 = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            col2 = st.selectbox("Y-axis", numeric_cols, key="scatter_y", 
                              index=min(1, len(numeric_cols)-1))
            fig = create_scatter_plot(df, col1, col2)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns")
    with tab5:
        st.markdown("### Data Heatmap")
        if len(numeric_cols) > 0:
            fig = create_data_heatmap(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)


def page_insights(df):
    st.markdown("## 🎯 Key Insights")
    display_quality_assessment(df)
    st.markdown("### Top Insights")
    insights = get_statistical_insights(df)
    display_insights_cards(insights)
    st.markdown("### Summary Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        summary_df = get_summary_statistics(df)
        st.dataframe(summary_df, use_container_width=True)


def page_preprocessing():
    st.markdown("## ⚙️ Data Preprocessing")

    if st.button("Apply Automatic Cleaning"):
        st.session_state.df_processed = clean_data(st.session_state.df_processed)
        st.success("✅ Automatic cleaning applied!")
        st.rerun()

    st.info("📋 Or, use the options below to clean and transform your data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Missing Values")
        handle_missing = st.checkbox("Handle missing values")
        if handle_missing:
            method = st.selectbox(
                "Method",
                ['drop', 'mean', 'median', 'ffill', 'bfill'],
                help="drop: Remove rows with missing values\nmean: Fill with mean\nmedian: Fill with median\nffill: Forward fill\nbfill: Backward fill"
            )
            threshold = st.slider("Drop columns if missing % > ", 0, 100, 50) / 100
            if st.button("Apply Missing Value Handling"):
                st.session_state.df_processed = handle_missing_values(st.session_state.df_processed, method=method, threshold=threshold)
                st.success(f"✅ Applied {method} method")
                st.rerun()
    with col2:
        st.markdown("### Duplicates")
        handle_dupes = st.checkbox("Remove duplicate rows")
        if handle_dupes:
            keep_option = st.radio("Keep", ['first', 'last'], help="Which duplicate to keep")
            if st.button("Remove Duplicates"):
                st.session_state.df_processed = remove_duplicates(st.session_state.df_processed, keep=keep_option)
                st.success("✅ Duplicates removed")
                st.rerun()
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Outliers")
        handle_outliers = st.checkbox("Remove outliers")
        if handle_outliers:
            method = st.selectbox("Method", ['iqr', 'zscore'], key="outlier_method")
            threshold = st.slider("Threshold", 1.0, 5.0, 1.5)
            numeric_cols = st.session_state.df_processed.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Columns to check", numeric_cols, default=numeric_cols[:3])
            if st.button("Remove Outliers"):
                st.session_state.df_processed = remove_outliers(st.session_state.df_processed, columns=selected_cols, method=method, threshold=threshold)
                st.success("✅ Outliers removed")
                st.rerun()
    with col4:
        st.markdown("### Feature Scaling")
        scale = st.checkbox("Scale features")
        if scale:
            method = st.selectbox("Scale Method", ['minmax', 'standard'], key="scale_method")
            numeric_cols = st.session_state.df_processed.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Columns to scale", numeric_cols, 
                                          default=numeric_cols[:3], key="scale_cols")
            if st.button("Apply Scaling"):
                st.session_state.df_processed = scale_features(st.session_state.df_processed, columns=selected_cols, method=method)
                st.success(f"✅ Applied {method} scaling")
                st.rerun()
    st.markdown("### Processed Data Preview")
    st.dataframe(st.session_state.df_processed.head(10), use_container_width=True)


def page_export(df):
    st.markdown("## 💾 Export Data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Export Formats")
        export_as_csv(df)
        export_as_excel(df)
    with col2:
        st.markdown("### Data Summary")
        display_data_summary(df)
    st.markdown("### Sample Data")
    n_rows = st.slider("Rows to display", 1, min(100, len(df)), 10)
    st.dataframe(df.head(n_rows), use_container_width=True)

