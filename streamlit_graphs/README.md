# Data Visualization Dashboard

A Streamlit-based interactive dashboard that lets you upload your own Excel or CSV file and instantly generate different types of charts — no sample data, no hardcoded datasets. Everything is driven by your file.

---

## Project Structure

```
streamlit_graphs/
│
├── graph_dashboard.py   # Main Streamlit app
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

---


## Supported File Formats

| Format | Extension |
|--------|-----------|
| Excel  | `.xlsx`, `.xls` |
| CSV    | `.csv` |

Multi-sheet Excel files are supported — a sheet selector will appear automatically in the sidebar.

---

##  Available Chart Types

| Chart | Best Used For |
|-------|--------------|
| **Bar Chart** | Comparing totals across categories |
| **Line Chart** | Trends over time or ordered values |
| **Scatter Plot** | Relationship between two numeric variables |
| **Pie / Donut Chart** | Part-to-whole proportions |
| **Histogram** | Distribution of a numeric column |
| **Box Plot** | Spread and outliers in numeric data |
| **Area Chart** | Cumulative or stacked trends over time |
| **Heatmap (Correlation)** | Correlation between all numeric columns |

---


##  Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data loading and manipulation |
| `plotly` | Interactive charts |
| `openpyxl` | Reading `.xlsx` Excel files |

Install all at once:

```bash
pip install -r requirements.txt
```

---

##  Download

After viewing your chart, expand the **"Download dataset as CSV"** section at the bottom of the page to download your loaded data.

---

### Common Issues

**App doesn't open automatically**
Run `streamlit run graph_dashboard.py` and manually open `http://localhost:8501` in your browser.

**`ModuleNotFoundError`**
Make sure you installed dependencies with `pip install -r requirements.txt` and your virtual environment is activated.

**Excel file not loading**
Ensure `openpyxl` is installed. It is required for `.xlsx` support.

**Date columns not detected**
The app auto-detects text columns that look like dates. If detection fails, convert the column to a proper date format in Excel before uploading.

---