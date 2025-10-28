# Dashboard Quick Start Guide

## 🚀 Launch in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements_dashboard.txt
```

### Step 2: Launch Dashboard
```bash
streamlit run dashboard.py
```

### Step 3: Open Browser
Dashboard automatically opens at: **http://localhost:8501**

---

## 📱 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│                 🤖 Template Harvester Dashboard              │
│              Analyzing 15,011 automation templates           │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│  SIDEBAR     │           MAIN CONTENT AREA                  │
│              │                                               │
│ 🔍 Filters:  │  📊 Overview  🔎 Explorer  📈 Analytics     │
│              │  🤖 AI Insights  🔗 Apps  🆚 Comparison      │
│ • Platform   │                                               │
│ • Auto Type  │  [Interactive Charts and Tables]              │
│ • Complexity │                                               │
│ • AI Filter  │  [Filters and Controls]                       │
│ • Popularity │                                               │
│ • App Range  │  [Data Visualizations]                        │
│              │                                               │
│ 📥 Export    │  [Analysis Results]                           │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 🎯 Top 5 Use Cases

### 1. **Find Perfect Template** (Explorer Tab)
```
1. Click "🔎 Explorer" tab
2. Enter search term (e.g., "email automation")
3. Set filters (complexity, industry, etc.)
4. Sort by engagement_score
5. Click template name to view details
```

### 2. **Understand AI Landscape** (AI Insights Tab)
```
1. Click "🤖 AI Insights" tab
2. View AI metrics dashboard
3. Explore use cases pie chart
4. Check provider distribution
5. Review top AI templates list
```

### 3. **Compare Templates** (Comparison Tab)
```
1. Click "🆚 Comparison" tab
2. Select Template 1 from dropdown
3. Select Template 2 from dropdown
4. Review side-by-side table
5. Analyze radar chart & features
```

### 4. **Analyze Trends** (Analytics Tab)
```
1. Click "📈 Analytics" tab
2. View scatter plot correlations
3. Check engagement by type
4. Compare platforms
5. Export filtered data
```

### 5. **Discover Popular Apps** (App Analysis Tab)
```
1. Click "🔗 App Analysis" tab
2. View category adoption chart
3. Check top 30 most used apps
4. Analyze integration patterns
5. Filter by app category in sidebar
```

---

## 🎨 Key Features

### Global Filters (Sidebar)
- **Platform**: Zapier, Make, n8n
- **Automation Type**: 11 categories
- **Complexity**: 4 levels
- **AI Filter**: All/Yes/No
- **Popularity**: 5 tiers
- **App Count**: Range slider

### Export Options
- Click "📥 Export Filtered Data"
- Downloads CSV with current filters applied
- Works from any tab

### Interactive Charts
- **Hover**: See detailed values
- **Click Legend**: Toggle series visibility
- **Zoom**: Drag to zoom, double-click to reset
- **Download**: Camera icon to save PNG

---

## 📊 Dashboard Tabs Overview

| Tab | Purpose | Key Charts |
|-----|---------|------------|
| **📊 Overview** | High-level metrics | Pie, Bar, Platform distribution |
| **🔎 Explorer** | Find templates | Searchable table, Detail view |
| **📈 Analytics** | Deep analysis | Scatter, Correlations, Trends |
| **🤖 AI Insights** | AI-specific data | AI use cases, Providers, Features |
| **🔗 App Analysis** | Integration data | Top apps, Categories, Patterns |
| **🆚 Comparison** | Side-by-side | Table, Radar, Feature matrix |

---

## 💡 Pro Tips

### Filtering Strategy
1. Start with **Platform** filter (if you prefer specific platform)
2. Add **Automation Type** for use case
3. Set **Complexity** based on skill level
4. Enable **AI Filter** if needed
5. Adjust **App Count** range to narrow results

### Discovery Workflow
```
Overview Tab
    ↓
(Understand dataset composition)
    ↓
Explorer Tab
    ↓
(Search & filter templates)
    ↓
AI Insights / App Analysis
    ↓
(Deep dive into specific areas)
    ↓
Comparison Tab
    ↓
(Compare shortlisted templates)
    ↓
Export
    ↓
(Download filtered results)
```

### Search Tips
- Use **partial matches**: "email" finds "email automation", "send email", etc.
- Search **app names**: "sheets" finds all Google Sheets templates
- Try **synonyms**: "chat" and "chatbot" may find different results

---

## 🎯 Example Queries

### Query 1: Beginner AI Projects
**Filters**:
- AI-Powered: Yes
- Complexity: BEGINNER
- Requires Coding: No

**Tab**: Explorer → Sort by engagement_score
**Result**: ~3,000 accessible AI templates

---

### Query 2: High-Impact Marketing
**Filters**:
- Automation Type: MARKETING
- Popularity: POPULAR, VIRAL
- Estimated Time Saved: 5_20HR_WEEK+

**Tab**: Analytics → View engagement
**Result**: ~150 high-ROI templates

---

### Query 3: Multi-App Workflows
**Filters**:
- App Count: 5-48 (use slider)
- Complexity: ADVANCED, EXPERT

**Tab**: App Analysis → Integration patterns
**Result**: ~500 complex workflows

---

## 🔧 Keyboard Shortcuts

While dashboard is running:
- **`R`** - Rerun the app
- **`C`** - Clear cache (if data changes)
- **`?`** - Show all shortcuts
- **`Ctrl+C`** - Stop dashboard (in terminal)

---

## ⚡ Performance Tips

### For Faster Loading:
1. Use **global filters** to reduce dataset size
2. **Clear cache** if switching datasets (Press `C`)
3. **Close unused tabs** in browser
4. **Restart dashboard** if slow: `Ctrl+C` then `streamlit run dashboard.py`

### For Better Analysis:
1. **Export data** for external tools (Excel, Python notebooks)
2. **Use comparison tool** instead of mental comparison
3. **Bookmark** specific filter combinations (browser bookmarks)
4. **Take screenshots** of charts for presentations

---

## 🐛 Quick Troubleshooting

### Dashboard Won't Start
```bash
# Check if Streamlit is installed
pip install streamlit

# Check if in correct directory
ls dashboard.py  # Should exist

# Check for errors
streamlit run dashboard.py  # Read error messages
```

### No Data Showing
```bash
# Generate enriched CSV
python enrich_unified_csv.py

# Verify file exists
ls exports/unified_templates_enriched_*.csv

# Restart dashboard
Ctrl+C → streamlit run dashboard.py
```

### Charts Not Loading
```bash
# Update dependencies
pip install --upgrade plotly streamlit pandas

# Clear browser cache
Ctrl+Shift+R (Chrome/Firefox)

# Clear Streamlit cache
Press 'C' in dashboard
```

### Filters Not Working
1. Check if values exist in dataset
2. Clear all filters and reapply one by one
3. Restart dashboard
4. Check sidebar shows "X templates match filters"

---

## 📚 Next Steps

### After Exploring Dashboard:

1. **Export Data** for deeper analysis in Excel/Python
2. **Screenshot Charts** for presentations
3. **Share Insights** with your team
4. **Regenerate Data** periodically:
   ```bash
   python scrape_zapier_production.py
   python scrape_make_production.py
   python scrape_n8n_production.py
   python create_unified_csv.py
   python enrich_unified_csv.py
   streamlit run dashboard.py
   ```

### Advanced Usage:

1. **Customize Dashboard**: Edit `dashboard.py` to add your charts
2. **Add New Filters**: Follow patterns in sidebar section
3. **Create Reports**: Export data + create custom visualizations
4. **Share Dashboard**: Deploy to Streamlit Cloud (free)

---

## 🎉 You're Ready!

Launch command:
```bash
streamlit run dashboard.py
```

Then open: **http://localhost:8501**

Happy analyzing! 🚀

---

**Questions?** Check `DASHBOARD_README.md` for detailed documentation.

**Data Issues?** Run `python test_dashboard.py` for diagnostics.

**Want to Customize?** Edit `dashboard.py` and press `R` to reload.
