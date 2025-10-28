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

### Prerequisites

**Important:** The enriched CSV file (50MB) is not included in the repository. You need to generate it first:

```bash
# 1. Scrape templates from all platforms (optional - or use existing CSVs)
python scrape_make_production.py
python scrape_n8n_production.py
python scrape_zapier_production.py

# 2. Create unified CSV
python create_unified_csv.py

# 3. Enrich the unified CSV with 43 additional columns
python enrich_unified_csv.py
```

This will generate `exports/unified_templates_enriched_YYYYMMDD_HHMMSS.csv` with 15,011+ templates.

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

**Repository:** https://github.com/harshit-codes/Template-Harvester

#### Step-by-Step Deployment:

1. **Fork the Repository** (optional) or use the main repo
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select:**
   - Repository: `harshit-codes/Template-Harvester` (or your fork)
   - Branch: `master`
   - Main file path: `dashboard.py`
6. **Click "Advanced settings"** and add:
   - Python version: `3.10` or higher
7. **Click "Deploy"**

#### Important: Data Setup for Cloud Deployment

Since the CSV file (50MB) is not in the repository, you have 3 options:

**Option 1: Upload CSV via GitHub (Recommended for testing)**
- Generate the CSV locally using the steps above
- Create a new branch
- Temporarily add the CSV: `git add -f exports/unified_templates_enriched_*.csv`
- Commit and push to your fork
- Deploy from that branch

**Option 2: Use Git LFS**
- Install Git LFS: `git lfs install`
- Track CSV files: `git lfs track "exports/*.csv"`
- Add and commit the CSV
- Push to GitHub (Git LFS will handle large files)

**Option 3: Generate CSV on Streamlit Cloud**
- Fork the repo
- Add a startup script that runs the enrichment process
- Note: This will take ~5-10 minutes on first deploy

Your dashboard will be live at `https://your-app-name.streamlit.app`

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
