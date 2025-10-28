#!/usr/bin/env python
"""
Create a unified CSV combining templates from all platforms (Zapier, Make, n8n)
- Merges all platform CSVs into a single file
- Validates data quality
- Removes duplicates
- Sorts by platform and popularity
- Generates summary statistics
"""
import csv
import os
from datetime import datetime
from collections import Counter
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)


def load_csv(filepath):
    """Load CSV file and return rows"""
    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}")
        return []

    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        logging.info(f"Loaded {len(rows):,} rows from {os.path.basename(filepath)}")
        return rows
    except Exception as e:
        logging.error(f"Error loading {filepath}: {e}")
        return []


def validate_row(row, platform):
    """Validate that a row has minimum required fields"""
    required_fields = ['platform', 'platform_id', 'name', 'url']

    for field in required_fields:
        if not row.get(field):
            return False

    # Check platform matches
    if row.get('platform') != platform:
        return False

    return True


def get_sort_key(row):
    """Generate sort key for templates"""
    platform = row.get('platform', 'zzz')

    # Get popularity metric (use views, usage_count, or 0)
    try:
        views = int(row.get('total_views') or 0)
    except:
        views = 0

    try:
        usage = int(row.get('usage_count') or 0)
    except:
        usage = 0

    popularity = max(views, usage)

    # Sort by platform (alphabetically), then by popularity (descending)
    return (platform, -popularity)


def generate_statistics(all_rows):
    """Generate statistics about the unified dataset"""
    stats = {
        'total_templates': len(all_rows),
        'by_platform': Counter(),
        'by_status': Counter(),
        'top_apps': Counter(),
        'with_creator': 0,
        'with_views': 0,
        'with_usage': 0,
        'public_templates': 0,
        'verified_creators': 0
    }

    for row in all_rows:
        platform = row.get('platform', 'unknown')
        stats['by_platform'][platform] += 1

        status = row.get('status', 'unknown')
        stats['by_status'][status] += 1

        # Count templates with various metrics
        if row.get('creator_name'):
            stats['with_creator'] += 1

        if row.get('total_views') and row.get('total_views') != '':
            stats['with_views'] += 1

        if row.get('usage_count') and row.get('usage_count') != '':
            stats['with_usage'] += 1

        if row.get('is_public') == 'True':
            stats['public_templates'] += 1

        if row.get('creator_verified') == 'True':
            stats['verified_creators'] += 1

        # Count apps used
        apps = row.get('apps_used', '')
        if apps:
            # Split by comma or semicolon
            app_list = [a.strip() for a in apps.replace(';', ',').split(',') if a.strip()]
            for app in app_list[:10]:  # Limit to first 10 apps per template
                stats['top_apps'][app] += 1

    return stats


def print_statistics(stats):
    """Print statistics report"""
    print("\n" + "=" * 80)
    print("  UNIFIED CSV STATISTICS")
    print("=" * 80)
    print()

    print(f"📊 Total Templates: {stats['total_templates']:,}")
    print()

    print("📦 By Platform:")
    for platform, count in sorted(stats['by_platform'].items()):
        percentage = (count / stats['total_templates'] * 100)
        print(f"   • {platform.upper()}: {count:,} ({percentage:.1f}%)")
    print()

    print("📈 Status Distribution:")
    for status, count in sorted(stats['by_status'].items()):
        percentage = (count / stats['total_templates'] * 100)
        print(f"   • {status}: {count:,} ({percentage:.1f}%)")
    print()

    print("📋 Data Coverage:")
    print(f"   • Templates with creator info: {stats['with_creator']:,} ({stats['with_creator']/stats['total_templates']*100:.1f}%)")
    print(f"   • Templates with view counts: {stats['with_views']:,} ({stats['with_views']/stats['total_templates']*100:.1f}%)")
    print(f"   • Templates with usage counts: {stats['with_usage']:,} ({stats['with_usage']/stats['total_templates']*100:.1f}%)")
    print(f"   • Public templates: {stats['public_templates']:,} ({stats['public_templates']/stats['total_templates']*100:.1f}%)")
    print(f"   • Verified creators: {stats['verified_creators']:,}")
    print()

    print("🔥 Top 20 Most Used Apps/Nodes:")
    for i, (app, count) in enumerate(stats['top_apps'].most_common(20), 1):
        print(f"   {i:2d}. {app}: {count:,} templates")
    print()


def main():
    # Print banner
    logging.info("=" * 80)
    logging.info("  CREATING UNIFIED CSV FROM ALL PLATFORMS")
    logging.info("=" * 80)
    logging.info("")

    # Define input files (use the latest/best files)
    input_files = {
        'zapier': './exports/zapier_templates_20251028_100630_2025-10-28_10-06-30.csv',
        'make': './exports/make_templates_20251028_104024_2025-10-28_10-40-24.csv',
        'n8n': './exports/n8n_templates_20251028_104701_2025-10-28_10-47-01.csv'
    }

    # Load all data
    logging.info("📥 Loading CSV files...")
    all_rows = []
    platform_counts = {}

    for platform, filepath in input_files.items():
        rows = load_csv(filepath)

        # Validate rows
        valid_rows = [row for row in rows if validate_row(row, platform)]
        invalid_count = len(rows) - len(valid_rows)

        if invalid_count > 0:
            logging.warning(f"   Skipped {invalid_count} invalid rows from {platform}")

        all_rows.extend(valid_rows)
        platform_counts[platform] = len(valid_rows)

    if not all_rows:
        logging.error("❌ No data to process!")
        return 1

    logging.info(f"✅ Loaded {len(all_rows):,} total templates")
    logging.info("")

    # Remove duplicates based on platform_id
    logging.info("🔍 Checking for duplicates...")
    seen_ids = set()
    unique_rows = []
    duplicates = 0

    for row in all_rows:
        platform_id = row.get('platform_id')
        if platform_id in seen_ids:
            duplicates += 1
            continue
        seen_ids.add(platform_id)
        unique_rows.append(row)

    if duplicates > 0:
        logging.warning(f"   Removed {duplicates} duplicate templates")
    else:
        logging.info("   No duplicates found")

    all_rows = unique_rows
    logging.info("")

    # Sort by platform and popularity
    logging.info("🔄 Sorting templates...")
    all_rows.sort(key=get_sort_key)
    logging.info("   Sorted by platform and popularity (views/usage)")
    logging.info("")

    # Generate statistics
    logging.info("📊 Generating statistics...")
    stats = generate_statistics(all_rows)
    print_statistics(stats)

    # Write unified CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'./exports/unified_templates_{timestamp}.csv'

    logging.info("💾 Writing unified CSV...")

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if all_rows:
                fieldnames = list(all_rows[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_rows)

        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)

        logging.info(f"✅ Unified CSV created successfully!")
        logging.info(f"   File: {output_file}")
        logging.info(f"   Size: {file_size_mb:.2f} MB")
        logging.info(f"   Templates: {len(all_rows):,}")
        logging.info("")

        # Summary by platform
        logging.info("📦 Templates per platform in unified CSV:")
        for platform, count in sorted(platform_counts.items()):
            logging.info(f"   • {platform.upper()}: {count:,}")
        logging.info("")

        logging.info("=" * 80)
        logging.info("  UNIFIED CSV CREATION COMPLETE")
        logging.info("=" * 80)

        return 0

    except Exception as e:
        logging.error(f"❌ Error writing unified CSV: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
