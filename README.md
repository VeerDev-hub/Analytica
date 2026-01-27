# 📊 Analytica Studio: AI-Powered Data Analysis

**Analytica Studio** is a powerful and intuitive Streamlit application designed for rapid data analysis and visualization. Upload your CSV or Excel files and instantly generate comprehensive overviews, detailed statistics, interactive visualizations, and actionable insights. The built-in preprocessing tools allow you to clean and transform your data on the fly.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://analytica-ftl3mjorytpnyjudve3deh.streamlit.app/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ Key Features

- **📊 Interactive Dashboard**: A clean and user-friendly interface for seamless data exploration.
- **📁 Multi-Format Support**: Upload data from both CSV and Excel files.
- **📝 Data Overview**: Get a quick glance at your dataset, including shape, data types, and missing values.
- **🔢 Descriptive Statistics**: Compute essential statistical measures like mean, median, standard deviation, and more.
- **📈 Rich Visualizations**:
  - **Histograms**: Understand the distribution of your data.
  - **Correlation Heatmaps**: Identify relationships between variables.
  - **Box Plots**: Spot outliers and data dispersion.
  - **Scatter Plots**: Visualize the relationship between two variables.
- **💡 Actionable Insights**: Automatically generated insights to highlight key characteristics of your data.
- **⚙️ Data Preprocessing**:
  - Handle missing values with various strategies (drop, mean, median, etc.).
  - Remove duplicate records.
  - Scale numerical features using `MinMaxScaler` or `StandardScaler`.
- **💾 Easy Export**: Download the cleaned and processed data as a new CSV or Excel file.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/VeerDev-hub/Analytica
    cd Analytica
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run data_analysis_app.py
    ```

2.  **Open your browser** and navigate to `http://localhost:8501`.

## 📁 Project Structure

```
.
├── data_analysis_app.py      # Main Streamlit application
├── pages.py                  # Functions for each page/tab
├── preprocessing.py          # Data cleaning and transformation functions
├── analytics.py              # Core data analysis functions
├── visualizations.py         # Plotting and visualization functions
├── ui_components.py          # UI helper functions
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.