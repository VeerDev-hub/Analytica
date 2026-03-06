import numpy as np
import pandas as pd
import streamlit as st

from analytics import (
    calculate_stats,
    detect_numeric_as_text,
    get_cardinality_warnings,
    get_column_info,
    get_data_quality_metrics,
    get_missing_data_analysis,
    get_null_hotspots,
    get_statistical_insights,
    get_summary_statistics,
)
from preprocessing import (
    clean_data,
    handle_missing_values,
    remove_duplicates,
    remove_outliers,
    scale_features,
)
from ui_components import (
    display_column_stats,
    display_data_preview,
    display_data_summary,
    display_insights_cards,
    display_metrics_row,
    display_quality_assessment,
    display_quality_metrics,
    export_as_csv,
    export_as_excel,
)
from visualizations import (
    create_bar_chart,
    create_box_plot,
    create_correlation_heatmap,
    create_data_heatmap,
    create_histogram,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot,
    get_chart_download_html,
)


def _render_chart_with_export(fig, chart_name):
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    st.download_button(
        f"Download {chart_name} as HTML",
        get_chart_download_html(fig),
        file_name=f"{chart_name.lower().replace(' ', '_')}.html",
        mime="text/html",
        key=f"download_{chart_name}",
    )


def _suggest_datetime_columns(df):
    candidates = []
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            candidates.append(col)
            continue
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().sum() >= max(3, int(len(df[col].dropna()) * 0.6)):
            candidates.append(col)
    return candidates


def _render_profiling_section(df):
    st.markdown("### Dataset Profiling")
    null_hotspots = get_null_hotspots(df)
    cardinality_warnings = get_cardinality_warnings(df)
    numeric_as_text = detect_numeric_as_text(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Null Hotspots", len(null_hotspots))
    c2.metric("Cardinality Warnings", len(cardinality_warnings))
    c3.metric("Numeric-as-Text Flags", len(numeric_as_text))

    tab1, tab2, tab3 = st.tabs(["Null Hotspots", "Cardinality", "Numeric as Text"])
    with tab1:
        if len(null_hotspots) > 0:
            st.dataframe(null_hotspots, use_container_width=True)
        else:
            st.success("No high-missing columns detected.")
    with tab2:
        if len(cardinality_warnings) > 0:
            st.dataframe(cardinality_warnings, use_container_width=True)
        else:
            st.success("No risky high-cardinality text columns detected.")
    with tab3:
        if len(numeric_as_text) > 0:
            st.dataframe(numeric_as_text, use_container_width=True)
        else:
            st.success("No suspicious numeric-as-text columns detected.")


def _render_sales_preset(df, numeric_cols, categorical_cols, datetime_cols):
    st.markdown("### Sales Preset")
    if not numeric_cols:
        st.warning("Sales preset needs at least one numeric column.")
        return

    date_col = st.selectbox("Date column", datetime_cols or [None], key="sales_date")
    value_col = st.selectbox("Revenue or value column", numeric_cols, key="sales_value")
    group_col = st.selectbox("Category column", categorical_cols or [None], key="sales_group")

    if date_col:
        sales_df = df.copy()
        sales_df[date_col] = pd.to_datetime(sales_df[date_col], errors="coerce")
        trend_df = sales_df.dropna(subset=[date_col]).sort_values(date_col)
        if not trend_df.empty:
            fig = create_line_chart(trend_df, date_col, value_col, title=f"{value_col} over time")
            _render_chart_with_export(fig, "Sales Trend")

    if group_col:
        grouped = df.groupby(group_col, dropna=False)[value_col].sum().reset_index().sort_values(value_col, ascending=False).head(12)
        fig = create_bar_chart(grouped, group_col, value_col, title=f"{value_col} by {group_col}")
        _render_chart_with_export(fig, "Sales Category Breakdown")


def _render_finance_preset(df, numeric_cols, datetime_cols):
    st.markdown("### Finance Preset")
    if len(numeric_cols) == 0:
        st.warning("Finance preset needs numeric columns.")
        return

    date_col = st.selectbox("Date column", datetime_cols or [None], key="finance_date")
    price_col = st.selectbox("Price column", numeric_cols, key="finance_price")
    volume_options = [None] + numeric_cols
    volume_col = st.selectbox("Volume column", volume_options, key="finance_volume")

    if date_col:
        finance_df = df.copy()
        finance_df[date_col] = pd.to_datetime(finance_df[date_col], errors="coerce")
        finance_df = finance_df.dropna(subset=[date_col]).sort_values(date_col)
        if not finance_df.empty:
            _render_chart_with_export(
                create_line_chart(finance_df, date_col, price_col, title=f"{price_col} trend"),
                "Finance Price Trend",
            )

            returns_df = finance_df[[date_col, price_col]].dropna().copy()
            returns_df["Return"] = returns_df[price_col].pct_change()
            returns_df = returns_df.dropna()
            if not returns_df.empty:
                _render_chart_with_export(
                    create_histogram(returns_df, "Return", title="Return distribution"),
                    "Finance Returns Distribution",
                )

            if volume_col:
                _render_chart_with_export(
                    create_bar_chart(finance_df, date_col, volume_col, title=f"{volume_col} by date"),
                    "Finance Volume View",
                )


def _render_survey_preset(df, numeric_cols, categorical_cols):
    st.markdown("### Survey Preset")
    if not categorical_cols and not numeric_cols:
        st.warning("Survey preset needs categorical or numeric columns.")
        return

    question_col = st.selectbox("Question or response column", categorical_cols or [None], key="survey_question")
    score_col = st.selectbox("Score column", [None] + numeric_cols, key="survey_score")
    segment_col = st.selectbox("Segment column", [None] + categorical_cols, key="survey_segment")

    if question_col:
        _render_chart_with_export(
            create_pie_chart(df, question_col, title=f"Response mix for {question_col}"),
            "Survey Response Mix",
        )

    if score_col:
        _render_chart_with_export(
            create_histogram(df, score_col, title=f"Distribution of {score_col}"),
            "Survey Score Distribution",
        )

    if score_col and segment_col:
        grouped = df.groupby(segment_col, dropna=False)[score_col].mean().reset_index().sort_values(score_col, ascending=False)
        _render_chart_with_export(
            create_bar_chart(grouped, segment_col, score_col, title=f"Average {score_col} by {segment_col}"),
            "Survey Segment Comparison",
        )


def page_overview(df):
    st.markdown("## Data Overview")
    display_metrics_row(df)
    display_data_preview(df)
    _render_profiling_section(df)
    st.markdown("### Column Information")
    st.dataframe(get_column_info(df), use_container_width=True)
    st.markdown("### Data Quality")
    display_quality_metrics(df)


def page_statistics(df):
    st.markdown("## Descriptive Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        st.error("No numeric columns detected.")
        st.markdown("### Debug Info")
        st.dataframe(get_column_info(df), use_container_width=True)
        st.markdown("### Tips")
        st.markdown(
            """
            - Check for letters or symbols mixed into numeric values.
            - Remove currency symbols or percentage signs before analysis.
            - Remove thousand separators if values were imported as text.
            - Check for leading or trailing spaces in numeric-looking cells.
            - Confirm numbers are not stored inside quoted strings.
            """
        )
        return

    st.dataframe(calculate_stats(df), use_container_width=True)
    st.markdown("### Column Deep Dive")
    selected_col = st.selectbox("Select column", numeric_cols)
    display_column_stats(df, selected_col)
    st.markdown("### Missing Data")
    missing_df = get_missing_data_analysis(df)

    if len(missing_df) > 0:
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("No missing values detected.")


def page_visualizations(df):
    st.markdown("## Data Visualizations")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = _suggest_datetime_columns(df)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Distributions", "Correlations", "Box Plots", "Scatter", "Heatmap", "Preset Views"]
    )

    with tab1:
        st.markdown("### Distribution Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="dist_col")
            bins = st.slider("Bins", 10, 100, 50, key="dist_bins")
            _render_chart_with_export(create_histogram(df, col, nbins=bins), "Histogram")
        else:
            st.warning("No numeric columns available.")

    with tab2:
        st.markdown("### Correlation Analysis")
        if len(numeric_cols) > 1:
            fig = create_correlation_heatmap(df)
            if fig:
                _render_chart_with_export(fig, "Correlation Heatmap")
        else:
            st.warning("At least two numeric columns are required.")

    with tab3:
        st.markdown("### Box Plot Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="box_col")
            _render_chart_with_export(create_box_plot(df, col), "Box Plot")
        else:
            st.warning("No numeric columns available.")

    with tab4:
        st.markdown("### Scatter Plot")
        if len(numeric_cols) > 1:
            col1 = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            col2 = st.selectbox("Y-axis", numeric_cols, key="scatter_y", index=min(1, len(numeric_cols) - 1))
            color_col = st.selectbox("Color by", [None] + categorical_cols, key="scatter_color")
            _render_chart_with_export(create_scatter_plot(df, col1, col2, color_col=color_col), "Scatter Plot")
        else:
            st.warning("At least two numeric columns are required.")

    with tab5:
        st.markdown("### Data Heatmap")
        if len(numeric_cols) > 0:
            fig = create_data_heatmap(df)
            if fig:
                _render_chart_with_export(fig, "Data Heatmap")
        else:
            st.warning("No numeric columns available.")

    with tab6:
        preset = st.selectbox("Preset view", ["Sales", "Finance", "Survey"])
        if preset == "Sales":
            _render_sales_preset(df, numeric_cols, categorical_cols, datetime_cols)
        elif preset == "Finance":
            _render_finance_preset(df, numeric_cols, datetime_cols)
        else:
            _render_survey_preset(df, numeric_cols, categorical_cols)


def page_insights(df):
    st.markdown("## Key Insights")
    display_quality_assessment(df)

    st.markdown("### Top Insights")
    display_insights_cards(get_statistical_insights(df))

    st.markdown("### Dataset Summary")
    quality = get_data_quality_metrics(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Completeness", f"{quality['completeness_score']:.1f}%")
    col2.metric("Uniqueness", f"{quality['uniqueness_score']:.1f}%")
    col3.metric("Memory Footprint", f"{quality['memory_usage_mb']:.2f} MB")

    st.markdown("### Profiling Findings")
    _render_profiling_section(df)

    st.markdown("### Summary Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.dataframe(get_summary_statistics(df), use_container_width=True)
    else:
        st.info("Summary statistics will appear once numeric columns are available.")


def page_preprocessing():
    st.markdown("## Data Preprocessing")

    if st.button("Apply Automatic Cleaning"):
        st.session_state.df_processed = clean_data(st.session_state.df_processed)
        st.success("Automatic cleaning applied.")
        st.rerun()

    st.info("Use the controls below to clean and transform the dataset step by step.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Missing Values")
        handle_missing = st.checkbox("Handle missing values")
        if handle_missing:
            method = st.selectbox(
                "Method",
                ["drop", "mean", "median", "ffill", "bfill"],
                help="Choose how missing values should be removed or filled.",
            )
            threshold = st.slider("Drop columns if missing % >", 0, 100, 50) / 100
            if st.button("Apply Missing Value Handling"):
                st.session_state.df_processed = handle_missing_values(
                    st.session_state.df_processed,
                    method=method,
                    threshold=threshold,
                )
                st.success(f"Applied {method} method.")
                st.rerun()

    with col2:
        st.markdown("### Duplicates")
        handle_dupes = st.checkbox("Remove duplicate rows")
        if handle_dupes:
            keep_option = st.radio("Keep", ["first", "last"], help="Choose which duplicate record to preserve.")
            if st.button("Remove Duplicates"):
                st.session_state.df_processed = remove_duplicates(
                    st.session_state.df_processed,
                    keep=keep_option,
                )
                st.success("Duplicates removed.")
                st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Outliers")
        handle_outliers = st.checkbox("Remove outliers")
        if handle_outliers:
            method = st.selectbox("Method", ["iqr", "zscore"], key="outlier_method")
            threshold = st.slider("Threshold", 1.0, 5.0, 1.5)
            numeric_cols = st.session_state.df_processed.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Columns to check", numeric_cols, default=numeric_cols[:3])
            if st.button("Remove Outliers"):
                st.session_state.df_processed = remove_outliers(
                    st.session_state.df_processed,
                    columns=selected_cols,
                    method=method,
                    threshold=threshold,
                )
                st.success("Outliers removed.")
                st.rerun()

    with col4:
        st.markdown("### Feature Scaling")
        scale = st.checkbox("Scale features")
        if scale:
            method = st.selectbox("Scale Method", ["minmax", "standard"], key="scale_method")
            numeric_cols = st.session_state.df_processed.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect(
                "Columns to scale",
                numeric_cols,
                default=numeric_cols[:3],
                key="scale_cols",
            )
            if st.button("Apply Scaling"):
                st.session_state.df_processed = scale_features(
                    st.session_state.df_processed,
                    columns=selected_cols,
                    method=method,
                )
                st.success(f"Applied {method} scaling.")
                st.rerun()

    st.markdown("### Processed Data Preview")
    st.dataframe(st.session_state.df_processed.head(10), use_container_width=True)


def page_export(df):
    st.markdown("## Export Data")
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
