import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Data Analysis Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
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

@st.cache_data
def load_data(uploaded_file):
    """Load data from uploaded file"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def get_column_info(df):
    """Get detailed column information"""
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
    """Calculate comprehensive statistics"""
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

def main():
    # Header
    st.markdown("# 📊 Data Analysis Studio")
    st.markdown("Fast local data analysis with instant results")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Max 100MB"
        )
        
        if uploaded_file is None:
            st.info("👈 Upload a file to get started!")
            return
        
        # Load data
        df = load_data(uploaded_file)
        if df is None:
            return
        
        st.success(f"✅ Loaded: {uploaded_file.name}")
        st.markdown(f"**Rows:** {df.shape[0]:,} | **Columns:** {df.shape[1]}")
        
        # Navigation
        st.markdown("## 🔍 Analysis Sections")
        page = st.radio(
            "Select Analysis",
            ["📊 Overview", "🔢 Statistics", "📈 Visualizations", "🎯 Insights", "💾 Export"],
            label_visibility="collapsed"
        )
    
    # Main content
    if page == "📊 Overview":
        show_overview(df)
    elif page == "🔢 Statistics":
        show_statistics(df)
    elif page == "📈 Visualizations":
        show_visualizations(df)
    elif page == "🎯 Insights":
        show_insights(df)
    elif page == "💾 Export":
        show_export(df)

def show_overview(df):
    """Overview tab"""
    st.markdown("## 📊 Data Overview")
    
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
    
    # Data Preview
    st.markdown("### Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Column Information
    st.markdown("### Column Information")
    col_info = get_column_info(df)
    st.dataframe(col_info, use_container_width=True)
    
    # Data Quality
    st.markdown("### Data Quality")
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

def show_statistics(df):
    """Statistics tab"""
    st.markdown("## 🔢 Descriptive Statistics")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found")
        return
    
    # Statistics table
    stats_df = calculate_stats(df)
    st.dataframe(stats_df, use_container_width=True)
    
    # Column-specific analysis
    st.markdown("### Deep Dive into Column")
    selected_col = st.selectbox("Select column", numeric_cols)
    
    col1, col2, col3, col4 = st.columns(4)
    series = df[selected_col].dropna()
    
    with col1:
        st.metric("Mean", f"{series.mean():.4f}")
    with col2:
        st.metric("Median", f"{series.median():.4f}")
    with col3:
        st.metric("Std Dev", f"{series.std():.4f}")
    with col4:
        st.metric("Range", f"{series.max() - series.min():.4f}")
    
    # Value distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Min Value", f"{series.min():.4f}")
    with col2:
        st.metric("Max Value", f"{series.max():.4f}")
    
    # Missing data analysis
    st.markdown("### Missing Data")
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing': df.isna().sum(),
        'Missing %': (df.isna().sum() / len(df) * 100).round(2)
    }).sort_values('Missing %', ascending=False)
    
    st.dataframe(missing_data[missing_data['Missing'] > 0], use_container_width=True)

def show_visualizations(df):
    """Visualizations tab"""
    st.markdown("## 📈 Data Visualizations")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Distributions", "Correlations", "Box Plots", "Scatter", "Heatmap"
    ])
    
    # Distributions
    with tab1:
        st.markdown("### Distribution Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="dist_col")
            
            fig = px.histogram(
                df,
                x=col,
                nbins=50,
                title=f"Distribution of {col}",
                labels={col: col, 'count': 'Frequency'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available")
    
    # Correlations
    with tab2:
        st.markdown("### Correlation Analysis")
        if len(numeric_cols) > 1:
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
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns")
    
    # Box Plots
    with tab3:
        st.markdown("### Box Plot Analysis")
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column", numeric_cols, key="box_col")
            
            fig = px.box(
                df,
                y=col,
                title=f"Box Plot of {col}",
                points="outliers"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available")
    
    # Scatter Plot
    with tab4:
        st.markdown("### Scatter Plot")
        if len(numeric_cols) > 1:
            col1 = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            col2 = st.selectbox("Y-axis", numeric_cols, key="scatter_y", index=min(1, len(numeric_cols)-1))
            
            fig = px.scatter(
                df,
                x=col1,
                y=col2,
                title=f"{col1} vs {col2}",
                opacity=0.7
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns")
    
    # Heatmap
    with tab5:
        st.markdown("### Data Heatmap")
        if len(numeric_cols) > 0:
            # Sample data if too large
            sample_df = df[numeric_cols].head(50)
            
            fig = px.imshow(
                sample_df.T,
                title="Data Heatmap (First 50 rows)",
                color_continuous_scale="Viridis",
                aspect="auto"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

def show_insights(df):
    """Insights tab"""
    st.markdown("## 🎯 Key Insights")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Completeness")
        completeness = (1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        st.metric("Completeness Score", f"{completeness:.1f}%")
        
        if completeness >= 95:
            st.success("✅ Excellent data quality")
        elif completeness >= 80:
            st.warning("⚠️ Some missing values")
        else:
            st.error("❌ Many missing values")
    
    with col2:
        st.markdown("### Uniqueness")
        duplicate_pct = (df.duplicated().sum() / len(df) * 100)
        st.metric("Unique Rows", f"{(100-duplicate_pct):.1f}%")
        
        if duplicate_pct == 0:
            st.success("✅ No duplicates found")
        elif duplicate_pct < 5:
            st.warning(f"⚠️ {duplicate_pct:.2f}% duplicates")
        else:
            st.error(f"❌ {duplicate_pct:.2f}% duplicates")
    
    # Top insights
    st.markdown("### Top Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        if len(numeric_cols) > 0:
            st.markdown("**Most Varied Column**")
            var_col = df[numeric_cols].std().idxmax()
            st.info(f"{var_col}: σ = {df[var_col].std():.4f}")
            
            st.markdown("**Least Varied Column**")
            var_col = df[numeric_cols].std().idxmin()
            st.info(f"{var_col}: σ = {df[var_col].std():.4f}")
    
    with insights_col2:
        if len(numeric_cols) > 0:
            st.markdown("**Most Correlated Pair**")
            corr_matrix = df[numeric_cols].corr()
            
            # Find max correlation (excluding diagonal)
            mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
            if mask.sum() > 0:
                max_corr_pair = corr_matrix.where(mask).stack().idxmax()
                max_corr_val = corr_matrix.loc[max_corr_pair]
                st.info(f"{max_corr_pair[0]} ↔ {max_corr_pair[1]}: {max_corr_val:.4f}")
    
    # Summary statistics
    st.markdown("### Summary Statistics")
    if len(numeric_cols) > 0:
        summary_df = df[numeric_cols].describe().T
        st.dataframe(summary_df, use_container_width=True)

def show_export(df):
    """Export tab"""
    st.markdown("## 💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Formats")
        
        # CSV Export
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Excel Export
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Download as Excel",
            data=excel_buffer.getvalue(),
            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col2:
        st.markdown("### Data Summary")
        summary_text = f"""
**File Summary**
- Rows: {df.shape[0]:,}
- Columns: {df.shape[1]}
- Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
- Complete: {(1 - df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%

**Column Types**
- Numeric: {df.select_dtypes(include=[np.number]).shape[1]}
- Text: {df.select_dtypes(include=['object']).shape[1]}
- Other: {df.select_dtypes(exclude=[np.number, 'object']).shape[1]}
"""
        st.markdown(summary_text)
    
    # Sample data
    st.markdown("### Sample Data")
    n_rows = st.slider("Rows to display", 1, min(100, len(df)), 10)
    st.dataframe(df.head(n_rows), use_container_width=True)

if __name__ == "__main__":
    main()
