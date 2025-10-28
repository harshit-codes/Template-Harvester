# 🤖 Template Harvester Dashboard

Interactive dashboard for analyzing **15,011 automation templates** from Make.com, n8n, and Zapier.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=harshit-codes/Template-Harvester&branch=master&mainModule=dashboard.py)

---

## 🚀 Quick Deploy

**Deploy to Streamlit Cloud in one click:**

👉 **[Deploy Now](https://share.streamlit.io/deploy?repository=harshit-codes/Template-Harvester&branch=master&mainModule=dashboard.py)**

---

## 📊 Dashboard Features

### 6 Interactive Tabs:

1. **📈 Overview** - Key metrics and distribution charts
   - Platform breakdown
   - Complexity levels
   - Technology adoption
   - Popular apps and integrations

2. **🔍 Explorer** - Advanced search and filtering
   - Real-time search across 15K templates
   - Multi-dimensional filters
   - Detailed template view
   - Export filtered results

3. **📊 Analytics** - Correlation and engagement analysis
   - App usage patterns
   - Complexity vs popularity
   - Platform comparisons

4. **🤖 AI Insights** - AI/ML adoption analysis
   - AI use case breakdown
   - Provider distribution
   - AI-powered template trends

5. **🔗 App Analysis** - Integration patterns
   - Top apps by category
   - Co-occurrence analysis
   - Workflow patterns

6. **⚖️ Comparison** - Side-by-side template comparison
   - Compare up to 3 templates
   - Feature comparison
   - Metric analysis

---

## 📈 Dataset

- **Total Templates:** 15,011
- **Platforms:** Make.com (53.4%), n8n (43.5%), Zapier (3.1%)
- **Unique Apps:** 1,346
- **AI-Powered:** 62% (9,303 templates)
- **Categorization:** 64 columns including automation types, complexity, industry, tech flags

---

## 🛠️ Local Setup

### Run Locally:

```bash
# Clone repository
git clone https://github.com/harshit-codes/Template-Harvester.git
cd Template-Harvester

# Install dependencies
pip install -r requirements_dashboard.txt

# Run dashboard
streamlit run dashboard.py
```

Dashboard will open at `http://localhost:8501`

---

## 📁 Project Structure

```
Template-Harvester/
├── dashboard.py                          # Main Streamlit dashboard
├── requirements_dashboard.txt            # Python dependencies
├── exports/
│   └── unified_templates_lite_*.csv     # Optimized dataset (31 MB)
├── DASHBOARD_README.md                   # Detailed dashboard docs
├── DASHBOARD_QUICKSTART.md               # Quick start guide
└── STREAMLIT_DEPLOYMENT.md               # Deployment guide
```

---

## 🎯 Use Cases

- **Market Research:** Analyze automation trends and popular integrations
- **Template Discovery:** Find templates by automation type, complexity, or technology
- **Competitive Analysis:** Compare platforms and understand ecosystem differences
- **Data Science:** Export filtered datasets for further analysis
- **AI/ML Insights:** Understand AI adoption in workflow automation

---

## 🔧 Tech Stack

- **Frontend:** Streamlit 1.28+
- **Visualization:** Plotly 5.17+
- **Data:** Pandas 2.0+
- **Python:** 3.9+

---

## 📊 Categorization

Each template is categorized across multiple dimensions:

### Primary Categories:
- **Automation Type:** AI_AUTOMATION, INTEGRATION, MARKETING, COMMUNICATION, etc.
- **Complexity Level:** BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
- **Industry:** IT, SALES, MARKETING, HR, ECOMMERCE, etc.
- **Integration Pattern:** SIMPLE_WORKFLOW, MULTI_STEP, HUB_AND_SPOKE, etc.
- **Popularity Tier:** VIRAL, POPULAR, MODERATE, NICHE

### Technology Flags:
- AI-powered, Webhook-based, Scheduled, Real-time
- Uses spreadsheet, email, CRM, communication tools
- Requires coding, API keys

---

## 🌟 Key Insights

### Top Apps (All Platforms):
1. **HTTP Request** - 3,088 templates (20.6%)
2. **Code** - 2,761 templates (18.4%)
3. **AI Agent** - 2,031 templates (13.5%)
4. **Google Sheets** - 1,807 templates (12.0%)
5. **OpenAI Chat Model** - 1,530 templates (10.2%)

### Top Use Cases:
1. Form Processing (6,725 templates)
2. File Management (3,603 templates)
3. Content Creation (2,513 templates)
4. Customer Support (1,909 templates)

### Complexity Distribution:
- Beginner: 55.7%
- Intermediate: 21.2%
- Advanced: 12.1%
- Expert: 11.0%

---

## 📝 Documentation

- **[Dashboard Quick Start](DASHBOARD_QUICKSTART.md)** - Get started in 5 minutes
- **[Deployment Guide](STREAMLIT_DEPLOYMENT.md)** - Deploy to Streamlit Cloud
- **[Categorization Analysis](CATEGORIZATION_ANALYSIS_20251028_142728.md)** - Detailed analysis report

---

## 🤝 Contributing

This project harvests public template data from automation platforms. To update the dataset:

1. Run scrapers for latest templates
2. Run enrichment script to add categorization
3. Create lite version for deployment
4. Push to GitHub (auto-deploys to Streamlit)

---

## 📄 License

This project analyzes publicly available template data. All trademarks and template content belong to their respective owners (Make.com, n8n, Zapier).

---

## 🙏 Acknowledgments

Data sourced from:
- **Make.com** - Visual workflow automation platform
- **n8n** - Open-source workflow automation
- **Zapier** - No-code automation platform

---

## 📧 Contact

Created with Claude Code - https://claude.ai/code

For issues or questions, please open a GitHub issue.

---

**Last Updated:** October 28, 2025
**Dataset Version:** 20251028
**Templates:** 15,011
**Status:** ✅ Production Ready
