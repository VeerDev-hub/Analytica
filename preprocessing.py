import pandas as pd
import numpy as np


def load_and_clean_data(uploaded_file):
    try:
        df = _load_file(uploaded_file)
        df = _fix_malformed_headers(df)
        df = _remove_empty_rows(df)
        df = _clean_column_names(df)
        df = _convert_numeric_columns(df)
        df = _reset_index(df)
        return df
    except Exception as e:
        raise Exception(f"Error loading file: {str(e)}")


def _load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file, engine='openpyxl')


def _fix_malformed_headers(df):
    if df.shape[0] > 2:
        first_col_vals = df.iloc[:2, 0].astype(str).str.lower()
        if 'ticker' in first_col_vals.values and 'date' in first_col_vals.values:
            df = df.iloc[2:].reset_index(drop=True)
            if 'price' in df.columns[0].lower() or 'date' in df.iloc[:5, 0].astype(str).str.lower().values:
                df = df.rename(columns={df.columns[0]: 'Date'})
                df['Date'] = df['Date'].astype(str)
    return df


def _remove_empty_rows(df):
    return df.dropna(how="all")


def _clean_column_names(df):
    df.columns = [str(col).strip() for col in df.columns]
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)
    df = df.loc[:, ~df.columns.duplicated(keep='first')]
    return df


def _convert_numeric_columns(df):
    for col in df.columns:
        if col.lower() in ['date', 'time', 'datetime']:
            continue
        try:
            converted = pd.to_numeric(df[col], errors='coerce')
            if converted.notna().sum() < len(df) * 0.5:
                try:
                    cleaned = df[col].astype(str).str.replace('[$%,]', '', regex=True).str.strip()
                    converted = pd.to_numeric(cleaned, errors='coerce')
                except:
                    pass
            if converted.notna().sum() >= len(df) * 0.5:
                df[col] = converted
        except:
            pass
    return df


def _reset_index(df):
    df.reset_index(drop=True, inplace=True)
    return df


def handle_missing_values(df, method='drop', threshold=0.5):
    df = df.copy()
    missing_pct = df.isna().sum() / len(df)
    cols_to_drop = missing_pct[missing_pct > threshold].index
    df = df.drop(columns=cols_to_drop)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if method == 'drop':
        df = df.dropna()
    elif method == 'mean':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif method == 'median':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif method == 'ffill':
        df = df.fillna(method='ffill')
    elif method == 'bfill':
        df = df.fillna(method='bfill')
    return df


def remove_duplicates(df, subset=None, keep='first'):
    return df.drop_duplicates(subset=subset, keep=keep)


def remove_outliers(df, columns=None, method='iqr', threshold=1.5):
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    for col in columns:
        if col not in df.columns:
            continue
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        elif method == 'zscore':
            from scipy import stats
            df = df[np.abs(stats.zscore(df[col].fillna(df[col].mean()))) < threshold]
    df.reset_index(drop=True, inplace=True)
    return df


def scale_features(df, columns=None, method='minmax'):
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    for col in columns:
        if col not in df.columns:
            continue
        if method == 'minmax':
            min_val = df[col].min()
            max_val = df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)
        elif method == 'standard':
            mean_val = df[col].mean()
            std_val = df[col].std()
            df[col] = (df[col] - mean_val) / std_val
    return df


def clean_data(df):
    df = df.copy()
    df = _remove_empty_rows(df)
    df = _clean_column_names(df)
    df = _convert_numeric_columns(df)
    df = _reset_index(df)
    return df
