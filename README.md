# Analytica Studio

Analytica Studio is a Streamlit app for fast local dataset analysis. Upload a CSV or Excel file and move through overview, statistics, visualizations, insights, preprocessing, and export workflows from a single interface.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## What It Does

- Upload CSV, XLSX, or XLS datasets.
- Profile data quality with null hotspots, high-cardinality warnings, and numeric-as-text detection.
- Explore descriptive statistics and dataset summaries.
- Build interactive charts with downloadable HTML exports.
- Use preset analysis views for sales, finance, and survey-style datasets.
- Clean data with missing-value handling, duplicate removal, outlier removal, and feature scaling.
- Export processed data as CSV or Excel.

## UI Notes

- The app adapts to light and dark device themes.
- Active navigation items use an orange highlight for clearer selection.
- Layout spacing was adjusted to reduce crowded controls and improve readability.

## Project Structure

```text
.
|-- data_analysis_app.py
|-- pages.py
|-- preprocessing.py
|-- analytics.py
|-- visualizations.py
|-- ui_components.py
|-- requirements.txt
`-- README.md
```

## Requirements

- Python 3.9+
- pip

## Installation

```bash
git clone https://github.com/VeerDev-hub/Analytica.git
cd Analytica
python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run data_analysis_app.py
```

Then open `http://localhost:8501`.

## Main App Pages

- `Overview`: dataset snapshot, metrics, profiling, and quality checks.
- `Statistics`: descriptive statistics, missing-data view, and numeric column deep dive.
- `Visualizations`: standard charts, chart export, and preset workflows.
- `Insights`: summary metrics, statistical insights, and profiling findings.
- `Preprocessing`: step-by-step cleaning and transformation controls.
- `Export`: processed dataset download and final summary.

## Implementation Notes

- File loading is cached with `st.cache_data` for faster reloads of larger datasets.
- Chart downloads are exported as standalone HTML files.
- Data cleaning includes automatic column-name cleanup and numeric coercion when possible.

## Repository

- GitHub: https://github.com/VeerDev-hub/Analytica
