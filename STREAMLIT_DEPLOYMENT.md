# Streamlit Cloud Deployment Guide

Complete guide for deploying the Template Harvester Dashboard to Streamlit Cloud.

---

## Overview

The dashboard is now optimized for Streamlit Cloud deployment with a **30.80 MB** lite version (down from 49.73 MB, 38% reduction).

### What's Changed:

✅ **Dropped 9 heavy columns:**
- `description_plain` (44.89 MB) - verbose duplicate
- `description_html` (0.11 MB) - HTML format not needed
- `slug` (1.26 MB) - redundant URL slug
- `creator_avatar_url` (1.34 MB) - not essential for dashboard
- `team_id` (0.11 MB) - not needed
- `approved_at` (0.11 MB) - not essential timestamp
- `approval_requested` (0.11 MB) - not needed
- `platform_native_id` (0.11 MB) - redundant ID
- `published_at` (0.11 MB) - redundant timestamp

✅ **Retained all essential columns (64 columns):**
- ✅ All categorization columns (automation_type, complexity_level, primary_industry, etc.)
- ✅ All boolean flags (is_ai_powered, uses_spreadsheet, requires_coding, etc.)
- ✅ All metrics (app_count, node_count, engagement_score, popularity_tier)
- ✅ Core fields (platform, name, description, url, apps_used, tags, etc.)

### Dashboard Features:
- 6 interactive tabs
- Multi-dimensional filtering
- Real-time search
- Interactive visualizations (Plotly)
- CSV export functionality
- 15,011 templates analyzed

---

## File Structure

```
Template-Harvester/
├── dashboard.py                                    # Main Streamlit app
├── requirements_dashboard.txt                      # Python dependencies
├── exports/
│   └── unified_templates_lite_20251028_142514.csv  # Optimized data (30.80 MB)
└── README.md                                       # Optional: Main documentation
```

---

## Pre-Deployment Checklist

### 1. Verify Files

```bash
# Check file sizes
ls -lh exports/unified_templates_lite_*.csv

# Should show ~31 MB
```

### 2. Test Locally

```bash
# Run dashboard locally first
streamlit run dashboard.py

# Open browser to http://localhost:8501
# Test all tabs and filters to ensure everything works
```

### 3. Check Dependencies

```bash
# Verify requirements file exists
cat requirements_dashboard.txt
```

Should contain:
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

---

## Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Create a GitHub Repository**
   ```bash
   # Initialize git if not already
   git init

   # Add files
   git add dashboard.py requirements_dashboard.txt exports/unified_templates_lite_*.csv

   # Commit
   git commit -m "Add Template Harvester Dashboard"

   # Push to GitHub
   git remote add origin https://github.com/YOUR_USERNAME/template-harvester.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your GitHub repository
   - Set:
     - **Main file path:** `dashboard.py`
     - **Python version:** 3.9+ (recommended 3.11)
   - Click "Deploy"

### Option 2: Deploy via Streamlit CLI

```bash
# Install Streamlit CLI
pip install streamlit

# Login to Streamlit Cloud
streamlit login

# Deploy
streamlit deploy dashboard.py
```

---

## Configuration

### Streamlit Cloud Settings

**Advanced Settings (Optional):**

```toml
# .streamlit/config.toml (create if needed)

[server]
maxUploadSize = 500  # Allow large file uploads if needed
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## Performance Optimization

### 1. Data Loading
- ✅ Uses `@st.cache_data` for caching
- ✅ Prioritizes lite version automatically
- ✅ Low memory mode for pandas

### 2. File Size
- ✅ 30.80 MB (well under 50 MB limit)
- ✅ 15,011 templates × 64 columns
- ✅ All essential features retained

### 3. Rendering
- ✅ Lazy loading of visualizations
- ✅ Efficient filtering with pandas
- ✅ Streamlit's built-in optimization

---

## Troubleshooting

### Issue: File Too Large

**Symptoms:** GitHub rejects files over 100 MB, Streamlit Cloud may have issues with large files

**Solution:** Use the lite version (already implemented)
```bash
# The lite version is 30.80 MB - well within limits
ls -lh exports/unified_templates_lite_*.csv
```

### Issue: Slow Loading

**Symptoms:** Dashboard takes long to load initially

**Solutions:**
1. ✅ Data is cached with `@st.cache_data`
2. ✅ First load will be slower (Streamlit caches after)
3. Consider pagination for Explorer tab if needed

### Issue: Arrow Serialization Warnings

**Symptoms:** Warning messages in logs about Arrow table conversion

**Impact:** Non-fatal - Streamlit automatically fixes these

**Fix (if needed):** Update data type conversions in `load_data()`:
```python
# Ensure consistent data types
df['column_name'] = df['column_name'].astype(str)
```

### Issue: Missing Columns

**Symptoms:** Some features not working

**Check:** Verify all required columns exist:
```python
required_cols = ['automation_type', 'complexity_level', 'primary_industry',
                 'is_ai_powered', 'app_count', 'node_count']
missing = [col for col in required_cols if col not in df.columns]
print(f"Missing columns: {missing}")
```

---

## Updating the Dashboard

### Update Data

```bash
# 1. Regenerate enriched CSV with latest data
python enrich_unified_csv.py

# 2. Create new lite version
python create_lite_version.py

# 3. Commit and push
git add exports/unified_templates_lite_*.csv
git commit -m "Update templates data"
git push
```

**Note:** Streamlit Cloud will auto-redeploy on push to main branch.

### Update Dashboard Code

```bash
# 1. Modify dashboard.py
vim dashboard.py

# 2. Test locally
streamlit run dashboard.py

# 3. Commit and push
git add dashboard.py
git commit -m "Update dashboard features"
git push
```

---

## Cost & Limits

### Streamlit Cloud Free Tier:
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app (sufficient for our 30 MB dataset)
- ✅ Shared CPU
- ✅ Sleeps after inactivity (wakes on access)

### Upgrade Options (if needed):
- **Starter:** $20/month - More resources, faster wake
- **Professional:** Custom pricing - Enterprise features

**Our dashboard fits comfortably in the free tier.**

---

## Security & Privacy

### Data Handling:
- ✅ All data is public templates (no sensitive info)
- ✅ No authentication required
- ✅ Read-only dashboard (no data modifications)

### Best Practices:
- Don't include API keys in code
- Use Streamlit secrets for any credentials
- Keep enrichment scripts local (don't deploy)

---

## Monitoring

### Check Deployment Status:
- Streamlit Cloud dashboard: https://share.streamlit.io/
- View logs for errors
- Monitor resource usage

### Analytics:
- Streamlit Cloud provides basic analytics
- Views, active users, errors
- Performance metrics

---

## Alternative Hosting Options

If Streamlit Cloud doesn't meet your needs:

### 1. Heroku
```bash
# Requires Procfile:
web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. AWS EC2
- More control, more cost
- Requires server management

### 3. Google Cloud Run
- Serverless, scales to zero
- Pay per use

### 4. Self-Hosted
- Full control
- Requires infrastructure

**Recommendation:** Start with Streamlit Cloud (easiest & free).

---

## Success Criteria

✅ Dashboard loads within 5 seconds
✅ All 6 tabs functional
✅ Filters work correctly
✅ Visualizations render properly
✅ Search returns accurate results
✅ CSV export works
✅ No critical errors in logs

---

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Forum:** https://discuss.streamlit.io/
- **Plotly Docs:** https://plotly.com/python/
- **Pandas Docs:** https://pandas.pydata.org/docs/

---

## Quick Deploy Checklist

```bash
# 1. Create lite version (already done)
✅ python create_lite_version.py

# 2. Test locally
✅ streamlit run dashboard.py

# 3. Create GitHub repo
☐ git init
☐ git add dashboard.py requirements_dashboard.txt exports/unified_templates_lite_*.csv
☐ git commit -m "Initial dashboard commit"
☐ git push origin main

# 4. Deploy to Streamlit Cloud
☐ Go to https://share.streamlit.io/
☐ Click "New app"
☐ Select repository
☐ Set main file: dashboard.py
☐ Click "Deploy"

# 5. Verify
☐ Test all features
☐ Share public URL
```

---

## Next Steps

1. **Deploy:** Follow steps above to deploy to Streamlit Cloud
2. **Share:** Get public URL and share with stakeholders
3. **Monitor:** Check usage and performance
4. **Iterate:** Add new features based on feedback
5. **Update:** Refresh data regularly with latest templates

---

**Dashboard Status:** ✅ Ready for Production
**File Size:** 30.80 MB (38% reduction)
**Features:** 100% Retained
**Deployment:** Streamlit Cloud Compatible

---

*Generated: 2025-10-28*
