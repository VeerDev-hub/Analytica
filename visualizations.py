import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


COLOR_SEQUENCE = ["#2563eb", "#0ea5e9", "#14b8a6", "#f59e0b", "#ef4444", "#8b5cf6"]


def _apply_consistent_layout(fig, height=500):
    fig.update_layout(
        height=height,
        template="plotly",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Trebuchet MS, Segoe UI, sans-serif"},
        title={"font": {"size": 18}},
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)", zeroline=False)
    return fig


def get_chart_download_html(fig):
    return pio.to_html(fig, include_plotlyjs="cdn", full_html=True).encode("utf-8")


def create_histogram(df, column, nbins=50, title=None):
    if title is None:
        title = f"Distribution of {column}"
    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        title=title,
        labels={column: column, "count": "Frequency"},
        color_discrete_sequence=[COLOR_SEQUENCE[0]],
    )
    return _apply_consistent_layout(fig)


def create_correlation_heatmap(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    corr_matrix = df[numeric_cols].corr()
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 10},
        )
    )
    fig.update_layout(title="Correlation Matrix")
    return _apply_consistent_layout(fig, height=600)


def create_box_plot(df, column, title=None):
    if title is None:
        title = f"Box Plot of {column}"
    fig = px.box(
        df,
        y=column,
        title=title,
        points="outliers",
        color_discrete_sequence=[COLOR_SEQUENCE[2]],
    )
    return _apply_consistent_layout(fig)


def create_scatter_plot(df, x_col, y_col, title=None, color_col=None):
    if title is None:
        title = f"{x_col} vs {y_col}"
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color=color_col,
        opacity=0.7,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    return _apply_consistent_layout(fig)


def create_data_heatmap(df, max_rows=50):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return None
    sample_df = df[numeric_cols].head(max_rows)
    fig = px.imshow(
        sample_df.T,
        title=f"Data Heatmap (First {len(sample_df)} rows)",
        color_continuous_scale="Blues",
        aspect="auto",
    )
    return _apply_consistent_layout(fig, height=600)


def create_line_chart(df, x_col, y_col, title=None):
    if title is None:
        title = f"{y_col} over {x_col}"
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        markers=True,
        color_discrete_sequence=[COLOR_SEQUENCE[0]],
    )
    return _apply_consistent_layout(fig)


def create_bar_chart(df, x_col, y_col, title=None):
    if title is None:
        title = f"{y_col} by {x_col}"
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=[COLOR_SEQUENCE[1]],
    )
    return _apply_consistent_layout(fig)


def create_pie_chart(df, column, title=None):
    if title is None:
        title = f"Distribution of {column}"
    value_counts = df[column].value_counts().head(12)
    fig = px.pie(
        values=value_counts.values,
        names=value_counts.index,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    return _apply_consistent_layout(fig)


def create_violin_plot(df, column, title=None):
    if title is None:
        title = f"Violin Plot of {column}"
    fig = px.violin(
        df,
        y=column,
        title=title,
        box=True,
        points="outliers",
        color_discrete_sequence=[COLOR_SEQUENCE[4]],
    )
    return _apply_consistent_layout(fig)


def create_pair_plot(df, columns=None):
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    columns = columns[:4]
    fig = px.scatter_matrix(df[columns], title="Pair Plot Matrix")
    return _apply_consistent_layout(fig, height=600)
