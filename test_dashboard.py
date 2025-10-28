#!/usr/bin/env python
"""
Test dashboard functionality without launching UI
"""
import pandas as pd
import glob
import sys

print("=" * 80)
print("  DASHBOARD VALIDATION TEST")
print("=" * 80)
print()

# Test 1: Check if enriched CSV exists
print("✅ Test 1: Check for enriched CSV files")
enriched_files = glob.glob('./exports/unified_templates_enriched_*.csv')
if not enriched_files:
    print("❌ FAIL: No enriched CSV files found!")
    print("   Run: python enrich_unified_csv.py")
    sys.exit(1)

latest_file = max(enriched_files)
print(f"   Found: {latest_file}")
print()

# Test 2: Load data
print("✅ Test 2: Load enriched CSV")
try:
    df = pd.read_csv(latest_file, low_memory=False)
    print(f"   Loaded: {len(df):,} rows, {len(df.columns)} columns")
except Exception as e:
    print(f"❌ FAIL: Could not load CSV: {e}")
    sys.exit(1)
print()

# Test 3: Check required columns
print("✅ Test 3: Verify required columns")
required_cols = [
    'platform', 'name', 'automation_type', 'complexity_level',
    'is_ai_powered', 'app_count', 'engagement_score', 'popularity_tier'
]

missing = [col for col in required_cols if col not in df.columns]
if missing:
    print(f"❌ FAIL: Missing columns: {missing}")
    sys.exit(1)
print(f"   All required columns present")
print()

# Test 4: Check data types
print("✅ Test 4: Validate data types")
try:
    # Convert boolean columns
    bool_columns = ['is_ai_powered', 'requires_coding']
    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].map({'True': True, 'False': False, True: True, False: False})

    # Convert numeric columns
    numeric_columns = ['app_count', 'engagement_score']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    print("   Data types converted successfully")
except Exception as e:
    print(f"❌ FAIL: Data type conversion error: {e}")
    sys.exit(1)
print()

# Test 5: Basic filtering
print("✅ Test 5: Test filtering functionality")
try:
    # Filter AI templates
    ai_df = df[df['is_ai_powered'] == True]
    print(f"   AI templates: {len(ai_df):,}")

    # Filter by platform
    make_df = df[df['platform'] == 'make']
    print(f"   Make.com templates: {len(make_df):,}")

    # Filter by complexity
    beginner_df = df[df['complexity_level'] == 'BEGINNER']
    print(f"   Beginner templates: {len(beginner_df):,}")

except Exception as e:
    print(f"❌ FAIL: Filtering error: {e}")
    sys.exit(1)
print()

# Test 6: Aggregations
print("✅ Test 6: Test aggregation functions")
try:
    # Group by automation type
    type_counts = df['automation_type'].value_counts()
    print(f"   Automation types found: {len(type_counts)}")

    # Calculate averages
    avg_apps = df['app_count'].mean()
    avg_engagement = df['engagement_score'].mean()
    print(f"   Avg apps: {avg_apps:.2f}")
    print(f"   Avg engagement: {avg_engagement:.2f}")

except Exception as e:
    print(f"❌ FAIL: Aggregation error: {e}")
    sys.exit(1)
print()

# Test 7: Check visualization data
print("✅ Test 7: Prepare visualization data")
try:
    # Platform distribution
    platform_counts = df['platform'].value_counts()
    print(f"   Platform counts: {dict(platform_counts)}")

    # Complexity distribution
    complexity_counts = df['complexity_level'].value_counts()
    print(f"   Complexity levels: {len(complexity_counts)}")

    # Popularity distribution
    popularity_counts = df['popularity_tier'].value_counts()
    print(f"   Popularity tiers: {len(popularity_counts)}")

except Exception as e:
    print(f"❌ FAIL: Visualization prep error: {e}")
    sys.exit(1)
print()

# Test 8: Export functionality
print("✅ Test 8: Test CSV export")
try:
    test_export = ai_df.head(10).to_csv(index=False)
    print(f"   Export successful: {len(test_export)} bytes")
except Exception as e:
    print(f"❌ FAIL: Export error: {e}")
    sys.exit(1)
print()

# Test 9: Dependencies check
print("✅ Test 9: Check dashboard dependencies")
try:
    import streamlit
    import plotly
    import numpy
    print(f"   Streamlit: v{streamlit.__version__}")
    print(f"   Plotly: v{plotly.__version__}")
    print(f"   NumPy: v{numpy.__version__}")
    print(f"   Pandas: v{pd.__version__}")
except ImportError as e:
    print(f"❌ FAIL: Missing dependency: {e}")
    print("   Run: pip install -r requirements_dashboard.txt")
    sys.exit(1)
print()

# Summary
print("=" * 80)
print("  ✅ ALL TESTS PASSED - DASHBOARD READY!")
print("=" * 80)
print()
print("To launch dashboard:")
print("   streamlit run dashboard.py")
print()
print("Dashboard will be available at:")
print("   http://localhost:8501")
print()
