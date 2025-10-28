# Template Harvester

A comprehensive data analysis dashboard for exploring **15,011 automation templates** from Zapier, Make.com, and n8n.

## 🚀 Live Dashboard

**Deploy to Streamlit Cloud** for free hosting - see [Deployment](#deployment) section below.

## 📊 Dashboard Features

- **15,011 Templates** across 3 platforms (Make: 53.4%, n8n: 43.5%, Zapier: 3.1%)
- **73 Enriched Columns** including AI detection, complexity scoring, popularity metrics
- **6 Interactive Tabs**: Overview, Explorer, Analytics, AI Insights, App Analysis, Comparison
- **Real-time Filtering** by platform, automation type, complexity, AI features
- **Interactive Visualizations** powered by Plotly
- **CSV Export** functionality

### Dashboard Insights
- 62% AI-powered templates (9,303)
- 55.7% beginner-friendly (8,368)
- Top apps: HTTP Request, Code, AI Agent, Google Sheets

## 🎯 Quick Start - Dashboard

### Installation

```bash
# Install dashboard dependencies
pip install -r requirements_dashboard.txt
```

### Run Locally

```bash
streamlit run dashboard.py
```

Dashboard opens at `http://localhost:8501`

### Documentation
- [Dashboard Quick Start Guide](DASHBOARD_QUICKSTART.md)
- [Dashboard README](DASHBOARD_README.md)
- [Enrichment README](ENRICHMENT_README.md)

## 🌐 Deployment

### Deploy to Streamlit Community Cloud (Free)

1. **Push to GitHub** (see instructions below)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select:**
   - Repository: `your-username/Template-Harvester`
   - Branch: `main` or `master`
   - Main file path: `dashboard.py`
6. **Click "Deploy"**

Your dashboard will be live at `https://your-app-name.streamlit.app`

**Note:** Since CSV files are large and excluded from git, you'll need to either:
- Upload a sample CSV to the repo, or
- Generate the enriched CSV on first run

---

## Template Scraper

Template Harvester is also a Python application designed to extract and consolidate automation templates from n8n, Make.com, and Zapier APIs into a unified CSV file.

## Features

- Fetches templates from n8n and Make.com.
- Normalizes disparate API responses into a unified CSV schema.
- Handles pagination and API rate limits.
- Exports data to a single, standardized CSV file.
- Configurable via `config.json`.

## Setup

1.  **Clone the repository (if applicable) or navigate to the project directory.**

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys and Settings:**

    Edit the `config.json` file in the root directory. You will need to provide your API keys/client IDs for Make.com and Zapier.

    ```json
    {
      "platforms": {
        "n8n": {
          "enabled": true,
          "base_url": "https://api.n8n.io",
          "max_pages": 10,
          "rows_per_page": 100
        },
        "make": {
          "enabled": true,
          "base_url": "https://eu1.make.com",
          "api_key": "YOUR_MAKE_API_KEY",
          "max_pages": 10,
          "limit": 100
        }
      },
      "output": {
        "format": "csv",
        "filename_prefix": "templates",
        "include_timestamp": true,
        "directory": "./exports"
      },
      "logging": {
        "level": "INFO",
        "file": "./logs/scraper.log",
        "console": true
      }
    }
    ```

    *   Replace `"YOUR_MAKE_API_KEY"` with your actual Make.com API key.

    **Note:** For Make.com, you typically obtain these credentials from your developer dashboard on their respective platforms.

## Running the Scraper

Execute the `main.py` script from the `template_harvester` directory:

```bash
python -m template_harvester.main
```

## Output

The generated CSV file(s) will be saved in the `./exports` directory (or the directory specified in `config.json`). Log files will be saved in `./logs`.

## Project Structure

```
.  
├── config.json  
├── requirements.txt  
└── template_harvester/  
    ├── __init__.py  
    ├── main.py  
    ├── config.py  
    ├── scrapers/  
    │   ├── __init__.py  
    │   ├── base_scraper.py  
    │   ├── n8n_scraper.py  
    │   ├── make_scraper.py  
    │   └── zapier_scraper.py  
    ├── normalizers/  
    │   ├── __init__.py  
    │   ├── base_normalizer.py  
    │   ├── n8n_normalizer.py  
    │   ├── make_normalizer.py  
    │   └── zapier_normalizer.py  
    ├── exporters/  
    │   ├── __init__.py  
    │   └── csv_exporter.py  
    └── utils/  
        ├── __init__.py  
        └── logging_setup.py  
```
