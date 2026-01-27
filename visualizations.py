import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_histogram(df, column, nbins=50, title=None):
    if title is None:
        title = f"Distribution of {column}"
    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        title=title,
        labels={column: column, 'count': 'Frequency'}
    )
    fig.update_layout(height=500)
    return fig


def create_correlation_heatmap(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    corr_matrix = df[numeric_cols].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    fig.update_layout(height=600, title="Correlation Matrix")
    return fig


def create_box_plot(df, column, title=None):
    if title is None:
        title = f"Box Plot of {column}"
    fig = px.box(
        df,
        y=column,
        title=title,
        points="outliers"
    )
    fig.update_layout(height=500)
    return fig


def create_scatter_plot(df, x_col, y_col, title=None, color_col=None):
    if title is None:
        title = f"{x_col} vs {y_col}"
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color=color_col,
        opacity=0.7
    )
    fig.update_layout(height=500)
    return fig


def create_data_heatmap(df, max_rows=50):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return None
    sample_df = df[numeric_cols].head(max_rows)
    fig = px.imshow(
        sample_df.T,
        title=f"Data Heatmap (First {len(sample_df)} rows)",
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    fig.update_layout(height=600)
    return fig


def create_line_chart(df, x_col, y_col, title=None):
    if title is None:
        title = f"{y_col} over {x_col}"
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        markers=True
    )
    fig.update_layout(height=500)
    return fig


def create_bar_chart(df, x_col, y_col, title=None):
    if title is None:
        title = f"{y_col} by {x_col}"
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title
    )
    fig.update_layout(height=500)
    return fig


def create_pie_chart(df, column, title=None):
    if title is None:
        title = f"Distribution of {column}"
    value_counts = df[column].value_counts()
    fig = px.pie(
        values=value_counts.values,
        names=value_counts.index,
        title=title
    )
    fig.update_layout(height=500)
    return fig


def create_violin_plot(df, column, title=None):
    if title is None:
        title = f"Violin Plot of {column}"
    fig = px.violin(
        df,
        y=column,
        title=title,
        box=True,
        points="outliers"
    )
    fig.update_layout(height=500)
    return fig


def create_pair_plot(df, columns=None):
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    columns = columns[:4]
    fig = px.scatter_matrix(
        df[columns],
        title="Pair Plot Matrix"
    )
    fig.update_layout(height=600, width=900)
    return fig
