import pandas as pd
import numpy as np
from scipy import stats


def get_column_info(df):
    info = []
    for col in df.columns:
        info.append({
            'Column': col,
            'Type': str(df[col].dtype),
            'Non-Null': df[col].notna().sum(),
            'Unique': df[col].nunique(),
            'Missing %': f"{(df[col].isna().sum() / len(df) * 100):.2f}%"
        })
    return pd.DataFrame(info)


def calculate_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_data = []
    for col in numeric_cols:
        series = df[col].dropna()
        stats_data.append({
            'Column': col,
            'Mean': f"{series.mean():.4f}",
            'Median': f"{series.median():.4f}",
            'Std Dev': f"{series.std():.4f}",
            'Min': f"{series.min():.4f}",
            'Q1': f"{series.quantile(0.25):.4f}",
            'Q3': f"{series.quantile(0.75):.4f}",
            'Max': f"{series.max():.4f}",
            'Skewness': f"{stats.skew(series):.4f}",
            'Kurtosis': f"{stats.kurtosis(series):.4f}"
        })
    return pd.DataFrame(stats_data)


def get_missing_data_analysis(df):
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing': df.isna().sum(),
        'Missing %': (df.isna().sum() / len(df) * 100).round(2)
    }).sort_values('Missing %', ascending=False)
    return missing_data[missing_data['Missing'] > 0]


def get_data_quality_metrics(df):
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isna().sum().sum()
    duplicate_rows = df.duplicated().sum()
    memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
    completeness = (1 - missing_cells / total_cells) * 100
    uniqueness = (1 - duplicate_rows / len(df)) * 100
    return {
        'total_rows': df.shape[0],
        'total_columns': df.shape[1],
        'numeric_columns': df.select_dtypes(include=[np.number]).shape[1],
        'categorical_columns': df.select_dtypes(include=['object']).shape[1],
        'missing_values': missing_cells,
        'missing_percentage': (missing_cells / total_cells * 100),
        'duplicate_rows': duplicate_rows,
        'duplicate_percentage': (duplicate_rows / len(df) * 100),
        'completeness_score': completeness,
        'uniqueness_score': uniqueness,
        'memory_usage_mb': memory_usage
    }


def get_correlation_matrix(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].corr()


def find_top_correlations(df, top_n=5):
    corr_matrix = get_correlation_matrix(df)
    mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
    correlations = []
    for i, col1 in enumerate(corr_matrix.columns):
        for j, col2 in enumerate(corr_matrix.columns):
            if i < j:
                correlations.append({
                    'Column 1': col1,
                    'Column 2': col2,
                    'Correlation': corr_matrix.loc[col1, col2]
                })
    df_corr = pd.DataFrame(correlations).sort_values('Correlation', ascending=False, key=abs)
    return df_corr.head(top_n)


def get_summary_statistics(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].describe().T


def get_column_distribution(df, column):
    return df[column].value_counts().reset_index()


def get_statistical_insights(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    insights = {}
    if len(numeric_cols) > 0:
        std_series = df[numeric_cols].std()
        insights['most_varied_column'] = {
            'column': std_series.idxmax(),
            'std_dev': std_series.max()
        }
        insights['least_varied_column'] = {
            'column': std_series.idxmin(),
            'std_dev': std_series.min()
        }
        corr_matrix = get_correlation_matrix(df)
        mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
        if mask.sum() > 0:
            max_corr_pair = corr_matrix.where(mask).stack().idxmax()
            max_corr_val = corr_matrix.loc[max_corr_pair]
            insights['most_correlated_pair'] = {
                'columns': max_corr_pair,
                'correlation': max_corr_val
            }
    return insights
