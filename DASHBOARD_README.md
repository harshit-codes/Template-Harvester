# Template Harvester - Interactive Dashboard

Comprehensive Streamlit dashboard for analyzing 15,000+ automation templates from Zapier, Make.com, and n8n.

## Quick Start

### Installation

```bash
# Install dashboard dependencies
pip install -r requirements_dashboard.txt
```

### Run Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## Features Overview

### 📊 **6 Comprehensive Tabs**

#### 1. **Overview Tab**
- **Key Metrics**: Total templates, AI-powered count, average apps, beginner-friendly count
- **Platform Distribution**: Pie chart showing template distribution across platforms
- **Automation Types**: Bar chart of top 10 automation categories
- **Complexity Distribution**: Visual breakdown by skill level
- **Popularity Distribution**: Templates by viral/popular/moderate/niche tiers
- **Technology Adoption**: Feature adoption rates (AI, webhooks, scheduling, etc.)

#### 2. **Explorer Tab**
- **Advanced Search**: Full-text search across names, descriptions, and apps
- **Multi-Filter Interface**: Filter by industry, setup time, coding requirements
- **Sort Options**: Sort by name, engagement, app count, complexity, popularity
- **Interactive Table**: Browse 15K+ templates with all key attributes
- **Template Details View**: Detailed information panel for selected templates
  - Basic info (name, platform, type, URL)
  - Technical details (complexity, setup time, requirements)
  - Popularity metrics (tier, engagement score, views)
  - Full description
  - Apps and integrations list

#### 3. **Analytics Tab**
- **Scatter Plot**: App count vs complexity correlation
- **Engagement Analysis**: Average engagement by automation type and complexity
- **Platform Comparison**: Side-by-side statistics for all platforms
- **Industry Analysis**: Template count and AI adoption by industry
- **Time Savings**: Funnel chart showing estimated weekly time savings
- **Trend Analysis**: Discover patterns and insights

#### 4. **AI Insights Tab**
- **AI Metrics Dashboard**: Count, percentage, LLM usage, RAG adoption
- **AI Use Cases**: Pie chart of AI applications (chatbots, content generation, etc.)
- **AI Providers**: Distribution across OpenAI, Google, Anthropic, etc.
- **AI Complexity**: How complex are AI templates?
- **Feature Adoption Matrix**: LLM, embeddings, vision, voice, memory, RAG
- **Top AI Templates**: Ranked by engagement score

#### 5. **App Analysis Tab**
- **App Category Adoption**: Usage of spreadsheets, email, storage, communication, etc.
- **Top 30 Most Used Apps**: Horizontal bar chart showing most popular integrations
- **App Count Distribution**: Histogram of templates by number of apps
- **Integration Patterns**: Pie chart showing workflow architectures

#### 6. **Comparison Tab**
- **Side-by-Side Comparison**: Compare any two templates
- **Attribute Table**: Line-by-line comparison of all key fields
- **Radar Chart**: Visual comparison of numeric metrics
- **Feature Matrix**: Bar chart showing feature availability

---

## Sidebar - Global Filters

### Available Filters:
- **Platform**: Select Zapier, Make, and/or n8n
- **Automation Type**: Filter by AI, Marketing, Communication, etc.
- **Complexity Level**: Beginner, Intermediate, Advanced, Expert
- **AI-Powered**: Show all, only AI, or non-AI templates
- **Popularity Tier**: Viral, Popular, Moderate, Niche
- **App Count Range**: Slider to filter by number of integrations

### Export Functionality:
- **Export Filtered Data**: Download current filtered dataset as CSV
- One-click export with all applied filters

---

## Key Visualizations

### Chart Types Used:
- **Pie Charts**: Platform distribution, AI use cases, integration patterns
- **Bar Charts**: Automation types, complexity levels, technology adoption
- **Scatter Plots**: Correlation analysis (app count vs complexity)
- **Line Charts**: Engagement trends by complexity
- **Funnel Charts**: Time savings distribution
- **Radar Charts**: Multi-metric template comparison
- **Grouped Bar Charts**: Feature comparison between templates
- **Histograms**: App count distribution

### Color Schemes:
- **Qualitative**: Set3, Viridis palettes for categories
- **Sequential**: Blues, Purples, Teal for single-variable intensity
- **Diverging**: RdYlGn for complexity (red=expert, green=beginner)

---

## Use Cases

### 1. **Template Discovery**
**Scenario**: Find beginner-friendly AI chatbots for customer support

**Steps**:
1. Go to Explorer tab
2. Set filters:
   - Automation Type: AI_AUTOMATION
   - Complexity: BEGINNER
   - Industry: CUSTOMER_SUPPORT
3. Search: "chatbot"
4. Sort by: engagement_score (descending)
5. Browse results and view details

---

### 2. **Market Research**
**Scenario**: Understand AI adoption across platforms

**Steps**:
1. Go to AI Insights tab
2. Review AI metrics and provider distribution
3. Go to Analytics tab
4. Check Platform Comparison table
5. Analyze industry-specific AI adoption

---

### 3. **Competitive Analysis**
**Scenario**: Compare two similar templates

**Steps**:
1. Go to Comparison tab
2. Select two templates from dropdowns
3. Review attribute comparison table
4. Analyze radar chart for numeric metrics
5. Check feature matrix for capabilities

---

### 4. **Trend Analysis**
**Scenario**: Identify most popular automation types

**Steps**:
1. Go to Overview tab
2. Review Automation Types bar chart
3. Go to Analytics tab
4. Check Engagement by Automation Type
5. Filter by Popularity: VIRAL, POPULAR
6. Export data for further analysis

---

### 5. **App Integration Planning**
**Scenario**: Find templates using specific apps

**Steps**:
1. Go to Explorer tab
2. Search: "google sheets" (or any app name)
3. Set additional filters as needed
4. Sort by engagement_score
5. View template details to see integration patterns

---

## Data Insights Examples

### What You Can Discover:

**Platform Insights**:
- Make.com has the most templates (53.4%)
- n8n has the richest metadata (creator info, views)
- Zapier templates are mostly interface-focused

**AI Insights**:
- 62% of templates are AI-powered
- OpenAI is the most popular provider (45%)
- Chatbots and content generation are top use cases

**Complexity Insights**:
- 55.7% are beginner-friendly
- Advanced templates have higher engagement scores
- Coding requirements present in ~18% of templates

**Technology Trends**:
- 52.7% use conditional logic
- 26.6% integrate with spreadsheets
- 17.8% are scheduled automations

**Popularity Patterns**:
- Only 1% achieve "viral" status (147 templates)
- 8.7% are "popular" (1,312 templates)
- AI templates trend higher in engagement

---

## Performance Optimization

### Data Caching:
- `@st.cache_data` decorator on data loading
- Loads data once, reuses across interactions
- Fast subsequent page loads

### Filtered Data:
- Sidebar filters apply globally
- Tab-specific filters build on global filters
- Real-time filtering without page reload

### Large Dataset Handling:
- Efficient pandas operations
- Plotly for interactive, GPU-accelerated charts
- Pagination in dataframe displays

---

## Customization

### Adding New Visualizations:

```python
# Example: Add a new chart
st.subheader("My Custom Chart")
fig = px.bar(
    filtered_df,
    x='automation_type',
    y='engagement_score',
    title='Custom Analysis'
)
st.plotly_chart(fig, use_container_width=True)
```

### Adding New Filters:

```python
# Example: Add a new filter in sidebar
new_filter = st.multiselect(
    "New Filter",
    options=df['some_column'].unique().tolist()
)

# Apply in filter_dataframe function
if new_filter:
    filtered_df = filtered_df[filtered_df['some_column'].isin(new_filter)]
```

### Adding New Tabs:

```python
# Add to tab list
tab1, tab2, ..., tab7 = st.tabs([
    "📊 Overview",
    ...
    "🆕 New Tab"
])

with tab7:
    st.header("New Analysis")
    # Your code here
```

---

## Troubleshooting

### **Dashboard won't start**
```bash
# Check if Streamlit is installed
pip install streamlit

# Check if dependencies are installed
pip install -r requirements_dashboard.txt
```

### **"No enriched CSV files found" error**
```bash
# Generate enriched CSV first
python enrich_unified_csv.py
```

### **Charts not displaying**
```bash
# Install/update plotly
pip install --upgrade plotly
```

### **Slow performance**
- Reduce data size using global filters
- Clear Streamlit cache: Click "☰ → Clear cache" in dashboard
- Restart dashboard: `Ctrl+C` then `streamlit run dashboard.py`

### **Data not updating**
- Regenerate enriched CSV
- Clear cache in dashboard
- Check if latest CSV file is being loaded

---

## Technical Details

### Technologies:
- **Streamlit**: Web framework (v1.28+)
- **Pandas**: Data manipulation (v2.0+)
- **Plotly**: Interactive visualizations (v5.17+)
- **NumPy**: Numerical operations (v1.24+)

### File Structure:
```
dashboard.py                    # Main dashboard application
requirements_dashboard.txt      # Python dependencies
DASHBOARD_README.md            # This file
exports/
  └── unified_templates_enriched_*.csv  # Data source
```

### Data Loading:
- Automatically finds latest enriched CSV
- Converts boolean columns to native Python booleans
- Converts numeric columns to proper types
- Handles missing values gracefully

### Layout:
- Wide layout for maximum screen space
- Sidebar for global filters
- Multi-tab interface for different analyses
- Responsive design adapts to screen size

---

## Advanced Features

### 1. **Data Export**
Export any filtered view to CSV for external analysis in Excel, Google Sheets, or data science tools.

### 2. **Real-time Filtering**
All filters apply immediately without page reload. Combine multiple filters for precise results.

### 3. **Interactive Charts**
- Hover for details
- Click legend items to toggle visibility
- Zoom, pan, and reset views
- Download charts as PNG

### 4. **Template Details**
Deep dive into any template with comprehensive details panel showing all 73 attributes.

### 5. **Comparison Tool**
Side-by-side comparison with visual radar chart and feature matrix.

---

## Keyboard Shortcuts

While in dashboard:
- **`R`**: Rerun the app
- **`C`**: Clear cache
- **`?`**: Show keyboard shortcuts
- **`Ctrl/Cmd + K`**: Search commands

---

## Best Practices

### For Analysis:
1. Start with Overview tab to understand the dataset
2. Use global filters to narrow focus
3. Export filtered data for deeper analysis
4. Compare templates to understand patterns
5. Use AI Insights for AI-specific discoveries

### For Template Discovery:
1. Use Explorer tab as main interface
2. Combine search with filters
3. Sort by engagement_score for popular templates
4. View template details before using
5. Export shortlist for team review

### For Presentations:
1. Use Overview charts for high-level insights
2. Analytics tab for detailed findings
3. Screenshot charts directly from browser
4. Export data to create custom visualizations
5. Use Comparison tool for feature showcases

---

## Updates & Maintenance

### To Update Data:
```bash
# 1. Regenerate unified CSV (if needed)
python create_unified_csv.py

# 2. Regenerate enriched CSV
python enrich_unified_csv.py

# 3. Dashboard will auto-load latest file
streamlit run dashboard.py
```

### To Update Dashboard:
- Edit `dashboard.py`
- Save file
- Dashboard auto-reloads (or press 'R')

---

## Example Queries

### Query 1: Find High-ROI Marketing Automations
**Filters**:
- Automation Type: MARKETING
- Estimated Time Saved: 5_20HR_WEEK, 20HR_PLUS_WEEK
- Popularity: POPULAR, VIRAL

**Result**: ~150 high-impact marketing templates

---

### Query 2: Beginner-Friendly AI Chatbots
**Filters**:
- AI-Powered: Yes
- AI Use Case: CHATBOT
- Complexity: BEGINNER
- Requires Coding: No

**Result**: ~800 accessible AI chatbot templates

---

### Query 3: Advanced Zapier Templates
**Filters**:
- Platform: Zapier
- Complexity: ADVANCED, EXPERT
- App Count: 4+

**Result**: ~50 complex Zapier workflows

---

## Support

For issues or questions:
- Check this README
- Review Streamlit documentation: https://docs.streamlit.io
- Check Plotly documentation: https://plotly.com/python/
- Review data source: Check enriched CSV

---

## Version History

**v1.0** (October 28, 2025)
- Initial release
- 6 comprehensive tabs
- 15K+ template analysis
- Interactive visualizations
- Export functionality
- Comparison tool

---

**Dashboard created with ❤️ for the automation community**

**Data**: 15,011 templates | 73 attributes | 3 platforms
**Performance**: Cached data loading | Real-time filtering | GPU-accelerated charts
**Status**: ✅ Production Ready
