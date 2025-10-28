#!/usr/bin/env python
"""
Template Harvester - Interactive Dashboard
Comprehensive Streamlit dashboard for analyzing 15K+ automation templates
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from collections import Counter
import glob
import os

# Page configuration
st.set_page_config(
    page_title="Template Harvester Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load enriched CSV data"""
    # Find latest enriched CSV
    enriched_files = glob.glob('./exports/unified_templates_enriched_*.csv')
    if not enriched_files:
        st.error("No enriched CSV files found! Please run enrich_unified_csv.py first.")
        st.stop()

    latest_file = max(enriched_files)

    # Load data
    df = pd.read_csv(latest_file, low_memory=False)

    # Convert boolean columns
    bool_columns = [
        'requires_coding', 'requires_api_keys', 'is_ai_powered',
        'is_webhook_based', 'is_scheduled', 'is_realtime',
        'has_conditional_logic', 'has_loops', 'uses_llm',
        'uses_embeddings', 'uses_vision', 'uses_voice', 'has_memory',
        'uses_spreadsheet', 'uses_email', 'uses_storage',
        'uses_communication', 'uses_crm', 'uses_social_media',
        'uses_ecommerce', 'uses_project_mgmt', 'uses_forms', 'has_rag'
    ]

    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].map({'True': True, 'False': False, True: True, False: False})

    # Convert numeric columns
    numeric_columns = ['app_count', 'node_count', 'engagement_score', 'total_views', 'usage_count']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df, latest_file


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_metric_card(title, value, delta=None):
    """Create a metric display card"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label=title, value=value, delta=delta)


def parse_json_field(value):
    """Parse JSON field safely"""
    if pd.isna(value) or value == '' or value is None:
        return []
    try:
        return json.loads(value)
    except:
        return []


def filter_dataframe(df, filters):
    """Apply filters to dataframe"""
    filtered = df.copy()

    for key, value in filters.items():
        if value is None or (isinstance(value, list) and len(value) == 0):
            continue

        if isinstance(value, list):
            if len(value) > 0:
                filtered = filtered[filtered[key].isin(value)]
        elif isinstance(value, tuple):  # Range filter
            filtered = filtered[
                (filtered[key] >= value[0]) & (filtered[key] <= value[1])
            ]
        elif isinstance(value, bool):
            filtered = filtered[filtered[key] == value]
        else:
            filtered = filtered[filtered[key] == value]

    return filtered


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Load data
    df, data_file = load_data()

    # Header
    st.markdown('<h1 class="main-header">🤖 Template Harvester Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>Analyzing {len(df):,} automation templates from Zapier, Make.com & n8n</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar - Global Filters
    with st.sidebar:
        st.header("🔍 Global Filters")

        # Platform filter
        platforms = st.multiselect(
            "Platform",
            options=df['platform'].unique().tolist(),
            default=df['platform'].unique().tolist()
        )

        # Automation type filter
        automation_types = st.multiselect(
            "Automation Type",
            options=sorted(df['automation_type'].dropna().unique().tolist()),
            default=[]
        )

        # Complexity filter
        complexity_levels = st.multiselect(
            "Complexity Level",
            options=['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'],
            default=[]
        )

        # AI-powered filter
        ai_filter = st.selectbox(
            "AI-Powered",
            options=['All', 'Yes', 'No']
        )

        # Popularity filter
        popularity_filter = st.multiselect(
            "Popularity Tier",
            options=['VIRAL', 'POPULAR', 'MODERATE', 'NICHE', 'UNKNOWN'],
            default=[]
        )

        # App count range
        st.subheader("App Count")
        app_count_range = st.slider(
            "Range",
            min_value=int(df['app_count'].min()),
            max_value=int(df['app_count'].max()),
            value=(int(df['app_count'].min()), int(df['app_count'].max()))
        )

        # Apply filters
        filters = {
            'platform': platforms if platforms else None,
            'automation_type': automation_types if automation_types else None,
            'complexity_level': complexity_levels if complexity_levels else None,
            'popularity_tier': popularity_filter if popularity_filter else None,
        }

        if ai_filter == 'Yes':
            filters['is_ai_powered'] = True
        elif ai_filter == 'No':
            filters['is_ai_powered'] = False

        filtered_df = filter_dataframe(df, filters)

        # Apply app count range
        filtered_df = filtered_df[
            (filtered_df['app_count'] >= app_count_range[0]) &
            (filtered_df['app_count'] <= app_count_range[1])
        ]

        st.markdown("---")
        st.info(f"**{len(filtered_df):,}** templates match filters")

        # Export button
        if st.button("📥 Export Filtered Data"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="filtered_templates.csv",
                mime="text/csv"
            )

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "🔎 Explorer",
        "📈 Analytics",
        "🤖 AI Insights",
        "🔗 App Analysis",
        "🆚 Comparison"
    ])

    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tab1:
        st.header("📊 Overview & Key Metrics")

        # Top metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Templates", f"{len(filtered_df):,}")

        with col2:
            ai_count = filtered_df['is_ai_powered'].sum()
            ai_pct = (ai_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.metric("AI-Powered", f"{ai_count:,}", f"{ai_pct:.1f}%")

        with col3:
            avg_apps = filtered_df['app_count'].mean()
            st.metric("Avg Apps", f"{avg_apps:.1f}")

        with col4:
            beginner_count = (filtered_df['complexity_level'] == 'BEGINNER').sum()
            st.metric("Beginner-Friendly", f"{beginner_count:,}")

        with col5:
            popular_count = filtered_df['popularity_tier'].isin(['VIRAL', 'POPULAR']).sum()
            st.metric("Popular Templates", f"{popular_count:,}")

        st.markdown("---")

        # Platform distribution
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Platform Distribution")
            platform_counts = filtered_df['platform'].value_counts()
            fig = px.pie(
                values=platform_counts.values,
                names=platform_counts.index,
                title="Templates by Platform",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Automation Types")
            auto_counts = filtered_df['automation_type'].value_counts().head(10)
            fig = px.bar(
                x=auto_counts.values,
                y=auto_counts.index,
                orientation='h',
                title="Top 10 Automation Types",
                labels={'x': 'Count', 'y': 'Type'},
                color=auto_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Complexity and Popularity
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Complexity Distribution")
            complexity_order = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']
            complexity_counts = filtered_df['complexity_level'].value_counts()
            complexity_counts = complexity_counts.reindex(complexity_order, fill_value=0)

            fig = px.bar(
                x=complexity_counts.index,
                y=complexity_counts.values,
                title="Templates by Complexity",
                labels={'x': 'Level', 'y': 'Count'},
                color=complexity_counts.values,
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Popularity Distribution")
            pop_order = ['VIRAL', 'POPULAR', 'MODERATE', 'NICHE', 'UNKNOWN']
            pop_counts = filtered_df['popularity_tier'].value_counts()
            pop_counts = pop_counts.reindex(pop_order, fill_value=0)

            fig = px.bar(
                x=pop_counts.index,
                y=pop_counts.values,
                title="Templates by Popularity",
                labels={'x': 'Tier', 'y': 'Count'},
                color=pop_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Technology adoption
        st.subheader("Technology Adoption")
        col1, col2, col3 = st.columns(3)

        tech_flags = {
            'is_ai_powered': 'AI-Powered',
            'is_webhook_based': 'Webhook-Based',
            'is_scheduled': 'Scheduled',
            'has_conditional_logic': 'Conditional Logic',
            'has_loops': 'Has Loops',
            'uses_llm': 'Uses LLM'
        }

        tech_data = []
        for col_name, label in tech_flags.items():
            if col_name in filtered_df.columns:
                count = filtered_df[col_name].sum()
                pct = (count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
                tech_data.append({'Technology': label, 'Count': count, 'Percentage': pct})

        tech_df = pd.DataFrame(tech_data)
        fig = px.bar(
            tech_df,
            x='Technology',
            y='Percentage',
            title='Technology Feature Adoption Rate',
            labels={'Percentage': 'Adoption %'},
            color='Percentage',
            color_continuous_scale='Teal'
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 2: EXPLORER
    # ========================================================================
    with tab2:
        st.header("🔎 Template Explorer")

        # Search
        search_term = st.text_input("🔍 Search templates", placeholder="Search by name, description, or apps...")

        # Additional filters
        col1, col2, col3 = st.columns(3)

        with col1:
            industry_filter = st.multiselect(
                "Industry",
                options=sorted(filtered_df['primary_industry'].dropna().unique().tolist())
            )

        with col2:
            setup_time_filter = st.multiselect(
                "Setup Time",
                options=['UNDER_5_MIN', '5_15_MIN', '15_30_MIN', '30_MIN_PLUS']
            )

        with col3:
            requires_coding_filter = st.selectbox(
                "Requires Coding",
                options=['All', 'Yes', 'No']
            )

        # Apply explorer filters
        explorer_df = filtered_df.copy()

        if search_term:
            search_lower = search_term.lower()
            explorer_df = explorer_df[
                explorer_df['name'].str.lower().str.contains(search_lower, na=False) |
                explorer_df['description'].str.lower().str.contains(search_lower, na=False) |
                explorer_df['apps_used'].str.lower().str.contains(search_lower, na=False)
            ]

        if industry_filter:
            explorer_df = explorer_df[explorer_df['primary_industry'].isin(industry_filter)]

        if setup_time_filter:
            explorer_df = explorer_df[explorer_df['estimated_setup_time'].isin(setup_time_filter)]

        if requires_coding_filter == 'Yes':
            explorer_df = explorer_df[explorer_df['requires_coding'] == True]
        elif requires_coding_filter == 'No':
            explorer_df = explorer_df[explorer_df['requires_coding'] == False]

        # Sort options
        col1, col2 = st.columns([3, 1])
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                options=['name', 'engagement_score', 'app_count', 'complexity_level', 'popularity_tier']
            )
        with col2:
            sort_order = st.radio("Order", options=['Ascending', 'Descending'], horizontal=True)

        explorer_df = explorer_df.sort_values(
            by=sort_by,
            ascending=(sort_order == 'Ascending')
        )

        st.info(f"Showing **{len(explorer_df):,}** templates")

        # Display templates
        display_columns = [
            'name', 'platform', 'automation_type', 'complexity_level',
            'app_count', 'popularity_tier', 'engagement_score', 'url'
        ]

        # Prepare display dataframe
        display_df = explorer_df[display_columns].copy()
        display_df = display_df.rename(columns={
            'name': 'Name',
            'platform': 'Platform',
            'automation_type': 'Type',
            'complexity_level': 'Complexity',
            'app_count': 'Apps',
            'popularity_tier': 'Popularity',
            'engagement_score': 'Score',
            'url': 'URL'
        })

        # Data editor for interactivity
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=600
        )

        # Template details expander
        st.subheader("Template Details")
        if len(explorer_df) > 0:
            selected_idx = st.selectbox(
                "Select template to view details",
                options=range(len(explorer_df)),
                format_func=lambda x: explorer_df.iloc[x]['name']
            )

            if selected_idx is not None:
                template = explorer_df.iloc[selected_idx]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Basic Info**")
                    st.write(f"**Name:** {template['name']}")
                    st.write(f"**Platform:** {template['platform'].upper()}")
                    st.write(f"**Type:** {template['automation_type']}")
                    st.write(f"**Subtype:** {template.get('automation_subtype', 'N/A')}")
                    st.write(f"**URL:** [{template['url']}]({template['url']})")

                with col2:
                    st.markdown("**Technical Details**")
                    st.write(f"**Complexity:** {template['complexity_level']}")
                    st.write(f"**Setup Time:** {template.get('estimated_setup_time', 'N/A')}")
                    st.write(f"**Apps Used:** {template['app_count']}")
                    st.write(f"**Requires Coding:** {'Yes' if template.get('requires_coding') else 'No'}")
                    st.write(f"**Is AI-Powered:** {'Yes' if template.get('is_ai_powered') else 'No'}")

                with col3:
                    st.markdown("**Popularity & Metrics**")
                    st.write(f"**Popularity:** {template.get('popularity_tier', 'UNKNOWN')}")
                    st.write(f"**Engagement Score:** {template.get('engagement_score', 0)}")
                    st.write(f"**Total Views:** {template.get('total_views', 'N/A')}")
                    st.write(f"**Usage Count:** {template.get('usage_count', 'N/A')}")

                st.markdown("**Description**")
                st.write(template.get('description', 'No description available')[:500] + "...")

                if template.get('apps_used'):
                    st.markdown("**Apps/Integrations**")
                    st.code(template['apps_used'])

    # ========================================================================
    # TAB 3: ANALYTICS
    # ========================================================================
    with tab3:
        st.header("📈 Advanced Analytics")

        # Correlation analysis
        st.subheader("App Count vs Complexity")
        fig = px.scatter(
            filtered_df,
            x='app_count',
            y='complexity_level',
            color='automation_type',
            size='engagement_score',
            hover_data=['name', 'platform'],
            title='Complexity vs App Count by Automation Type',
            category_orders={'complexity_level': ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Engagement analysis
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Engagement by Automation Type")
            avg_engagement = filtered_df.groupby('automation_type')['engagement_score'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=avg_engagement.values,
                y=avg_engagement.index,
                orientation='h',
                title='Average Engagement Score by Type',
                labels={'x': 'Avg Engagement Score', 'y': 'Automation Type'},
                color=avg_engagement.values,
                color_continuous_scale='Purples'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Engagement by Complexity")
            engagement_by_complexity = filtered_df.groupby('complexity_level')['engagement_score'].mean()
            engagement_by_complexity = engagement_by_complexity.reindex(['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'])

            fig = px.line(
                x=engagement_by_complexity.index,
                y=engagement_by_complexity.values,
                title='Average Engagement by Complexity',
                labels={'x': 'Complexity Level', 'y': 'Avg Engagement Score'},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

        # Platform comparison
        st.subheader("Platform Comparison")

        platform_stats = filtered_df.groupby('platform').agg({
            'platform_id': 'count',
            'is_ai_powered': 'sum',
            'app_count': 'mean',
            'engagement_score': 'mean',
            'complexity_level': lambda x: (x == 'BEGINNER').sum()
        }).round(2)

        platform_stats.columns = ['Total Templates', 'AI-Powered', 'Avg Apps', 'Avg Engagement', 'Beginner Templates']

        st.dataframe(platform_stats, use_container_width=True)

        # Industry analysis
        st.subheader("Industry Distribution & Engagement")
        industry_data = filtered_df.groupby('primary_industry').agg({
            'platform_id': 'count',
            'engagement_score': 'mean',
            'is_ai_powered': lambda x: (x == True).sum()
        }).sort_values('platform_id', ascending=False).head(10)

        industry_data.columns = ['Count', 'Avg Engagement', 'AI-Powered']

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Template Count by Industry', 'AI Adoption by Industry'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )

        fig.add_trace(
            go.Bar(x=industry_data.index, y=industry_data['Count'], name='Count'),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(x=industry_data.index, y=industry_data['AI-Powered'], name='AI-Powered', marker_color='lightblue'),
            row=1, col=2
        )

        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500, showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

        # Time-saving analysis
        st.subheader("Estimated Time Savings Distribution")
        time_saved_counts = filtered_df['estimated_time_saved'].value_counts()
        time_saved_order = ['UNDER_1HR_WEEK', '1_5HR_WEEK', '5_20HR_WEEK', '20HR_PLUS_WEEK']
        time_saved_counts = time_saved_counts.reindex(time_saved_order, fill_value=0)

        fig = px.funnel(
            y=time_saved_counts.index,
            x=time_saved_counts.values,
            title='Templates by Time Savings Potential'
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 4: AI INSIGHTS
    # ========================================================================
    with tab4:
        st.header("🤖 AI-Powered Template Insights")

        ai_df = filtered_df[filtered_df['is_ai_powered'] == True]

        if len(ai_df) == 0:
            st.warning("No AI-powered templates in current filters")
        else:
            # AI metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("AI Templates", f"{len(ai_df):,}")

            with col2:
                ai_pct = (len(ai_df) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
                st.metric("% of Total", f"{ai_pct:.1f}%")

            with col3:
                llm_count = ai_df['uses_llm'].sum() if 'uses_llm' in ai_df.columns else 0
                st.metric("Uses LLM", f"{llm_count:,}")

            with col4:
                rag_count = ai_df['has_rag'].sum() if 'has_rag' in ai_df.columns else 0
                st.metric("Uses RAG", f"{rag_count:,}")

            # AI use cases
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("AI Use Cases")
                ai_use_cases = ai_df['ai_use_case'].value_counts().head(10)
                fig = px.pie(
                    values=ai_use_cases.values,
                    names=ai_use_cases.index,
                    title="Distribution of AI Use Cases"
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("AI Providers")
                ai_providers = ai_df['ai_provider'].value_counts()
                fig = px.bar(
                    x=ai_providers.index,
                    y=ai_providers.values,
                    title="AI Provider Distribution",
                    labels={'x': 'Provider', 'y': 'Count'},
                    color=ai_providers.values,
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)

            # AI complexity
            st.subheader("AI Template Complexity")
            ai_complexity = ai_df['complexity_level'].value_counts()
            complexity_order = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']
            ai_complexity = ai_complexity.reindex(complexity_order, fill_value=0)

            fig = px.bar(
                x=ai_complexity.index,
                y=ai_complexity.values,
                title='AI Templates by Complexity',
                labels={'x': 'Complexity', 'y': 'Count'},
                color=ai_complexity.values,
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)

            # AI features matrix
            st.subheader("AI Feature Adoption")
            ai_features = {
                'Uses LLM': ai_df['uses_llm'].sum() if 'uses_llm' in ai_df.columns else 0,
                'Uses Embeddings': ai_df['uses_embeddings'].sum() if 'uses_embeddings' in ai_df.columns else 0,
                'Uses Vision': ai_df['uses_vision'].sum() if 'uses_vision' in ai_df.columns else 0,
                'Uses Voice': ai_df['uses_voice'].sum() if 'uses_voice' in ai_df.columns else 0,
                'Has Memory': ai_df['has_memory'].sum() if 'has_memory' in ai_df.columns else 0,
                'Has RAG': ai_df['has_rag'].sum() if 'has_rag' in ai_df.columns else 0
            }

            fig = go.Figure(data=[
                go.Bar(
                    x=list(ai_features.keys()),
                    y=list(ai_features.values()),
                    marker_color='lightseagreen'
                )
            ])
            fig.update_layout(
                title='AI Feature Adoption Count',
                xaxis_title='Feature',
                yaxis_title='Number of Templates'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top AI templates
            st.subheader("Top 10 Most Popular AI Templates")
            top_ai = ai_df.nlargest(10, 'engagement_score')[['name', 'ai_use_case', 'ai_provider', 'engagement_score', 'popularity_tier']]
            st.dataframe(top_ai, use_container_width=True, hide_index=True)

    # ========================================================================
    # TAB 5: APP ANALYSIS
    # ========================================================================
    with tab5:
        st.header("🔗 App & Integration Analysis")

        # App category adoption
        st.subheader("App Category Adoption")

        app_categories = {
            'Spreadsheet': filtered_df['uses_spreadsheet'].sum() if 'uses_spreadsheet' in filtered_df.columns else 0,
            'Email': filtered_df['uses_email'].sum() if 'uses_email' in filtered_df.columns else 0,
            'Storage': filtered_df['uses_storage'].sum() if 'uses_storage' in filtered_df.columns else 0,
            'Communication': filtered_df['uses_communication'].sum() if 'uses_communication' in filtered_df.columns else 0,
            'CRM': filtered_df['uses_crm'].sum() if 'uses_crm' in filtered_df.columns else 0,
            'Social Media': filtered_df['uses_social_media'].sum() if 'uses_social_media' in filtered_df.columns else 0,
            'E-commerce': filtered_df['uses_ecommerce'].sum() if 'uses_ecommerce' in filtered_df.columns else 0,
            'Project Mgmt': filtered_df['uses_project_mgmt'].sum() if 'uses_project_mgmt' in filtered_df.columns else 0,
            'Forms': filtered_df['uses_forms'].sum() if 'uses_forms' in filtered_df.columns else 0
        }

        fig = go.Figure(data=[
            go.Bar(
                x=list(app_categories.keys()),
                y=list(app_categories.values()),
                marker_color='indianred'
            )
        ])
        fig.update_layout(
            title='App Category Usage',
            xaxis_title='Category',
            yaxis_title='Number of Templates',
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)

        # Most used apps
        st.subheader("Most Frequently Used Apps")

        # Extract all apps
        all_apps = []
        for apps_str in filtered_df['apps_used'].dropna():
            if apps_str:
                apps = [a.strip() for a in str(apps_str).replace(';', ',').split(',') if a.strip()]
                all_apps.extend(apps[:10])  # Limit to first 10 apps per template

        app_counts = Counter(all_apps)
        top_apps = dict(app_counts.most_common(30))

        fig = px.bar(
            x=list(top_apps.values()),
            y=list(top_apps.keys()),
            orientation='h',
            title='Top 30 Most Used Apps',
            labels={'x': 'Number of Templates', 'y': 'App/Integration'},
            color=list(top_apps.values()),
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=800)
        st.plotly_chart(fig, use_container_width=True)

        # App count distribution
        st.subheader("App Count Distribution")

        app_count_dist = filtered_df['app_count'].value_counts().sort_index()

        fig = px.histogram(
            filtered_df,
            x='app_count',
            nbins=20,
            title='Distribution of App Count per Template',
            labels={'app_count': 'Number of Apps', 'count': 'Number of Templates'},
            color_discrete_sequence=['steelblue']
        )
        st.plotly_chart(fig, use_container_width=True)

        # Integration patterns
        st.subheader("Integration Patterns")
        pattern_counts = filtered_df['integration_pattern'].value_counts()

        fig = px.pie(
            values=pattern_counts.values,
            names=pattern_counts.index,
            title="Distribution of Integration Patterns"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 6: COMPARISON
    # ========================================================================
    with tab6:
        st.header("🆚 Template Comparison Tool")

        st.write("Select templates to compare side-by-side")

        # Template selection
        col1, col2 = st.columns(2)

        template_options = filtered_df['name'].tolist()

        with col1:
            template1_name = st.selectbox("Template 1", options=template_options, key='t1')

        with col2:
            template2_name = st.selectbox("Template 2", options=template_options, key='t2')

        if template1_name and template2_name:
            template1 = filtered_df[filtered_df['name'] == template1_name].iloc[0]
            template2 = filtered_df[filtered_df['name'] == template2_name].iloc[0]

            # Comparison table
            comparison_fields = [
                ('Platform', 'platform'),
                ('Automation Type', 'automation_type'),
                ('Subtype', 'automation_subtype'),
                ('Industry', 'primary_industry'),
                ('Complexity', 'complexity_level'),
                ('Setup Time', 'estimated_setup_time'),
                ('App Count', 'app_count'),
                ('AI-Powered', 'is_ai_powered'),
                ('Requires Coding', 'requires_coding'),
                ('Popularity Tier', 'popularity_tier'),
                ('Engagement Score', 'engagement_score'),
                ('Trigger Type', 'primary_trigger_type'),
                ('Action Type', 'primary_action_type'),
                ('Estimated Time Saved', 'estimated_time_saved')
            ]

            comparison_data = []
            for label, field in comparison_fields:
                val1 = template1.get(field, 'N/A')
                val2 = template2.get(field, 'N/A')

                # Format booleans
                if isinstance(val1, bool):
                    val1 = 'Yes' if val1 else 'No'
                if isinstance(val2, bool):
                    val2 = 'Yes' if val2 else 'No'

                comparison_data.append({
                    'Attribute': label,
                    template1_name: val1,
                    template2_name: val2
                })

            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

            # Visual comparison
            st.subheader("Visual Comparison")

            # Radar chart for numeric metrics
            categories = ['App Count', 'Engagement Score', 'Node Count']

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=[
                    template1.get('app_count', 0),
                    template1.get('engagement_score', 0),
                    template1.get('node_count', 0)
                ],
                theta=categories,
                fill='toself',
                name=template1_name
            ))

            fig.add_trace(go.Scatterpolar(
                r=[
                    template2.get('app_count', 0),
                    template2.get('engagement_score', 0),
                    template2.get('node_count', 0)
                ],
                theta=categories,
                fill='toself',
                name=template2_name
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Numeric Metrics Comparison"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Feature comparison
            st.subheader("Feature Comparison")

            features = [
                ('AI-Powered', 'is_ai_powered'),
                ('Webhook-Based', 'is_webhook_based'),
                ('Scheduled', 'is_scheduled'),
                ('Real-time', 'is_realtime'),
                ('Conditional Logic', 'has_conditional_logic'),
                ('Has Loops', 'has_loops'),
                ('Uses LLM', 'uses_llm'),
                ('Uses Spreadsheet', 'uses_spreadsheet'),
                ('Uses Email', 'uses_email'),
                ('Uses Communication', 'uses_communication')
            ]

            feature_data = []
            for label, field in features:
                t1_val = 1 if template1.get(field) == True else 0
                t2_val = 1 if template2.get(field) == True else 0
                feature_data.append({
                    'Feature': label,
                    template1_name: t1_val,
                    template2_name: t2_val
                })

            feature_df = pd.DataFrame(feature_data)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=feature_df['Feature'],
                y=feature_df[template1_name],
                name=template1_name
            ))
            fig.add_trace(go.Bar(
                x=feature_df['Feature'],
                y=feature_df[template2_name],
                name=template2_name
            ))

            fig.update_layout(
                barmode='group',
                title='Feature Availability (1=Yes, 0=No)',
                xaxis_tickangle=45
            )
            st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Template Harvester Dashboard v1.0</p>
        <p>Data Source: {os.path.basename(data_file)}</p>
        <p>Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
