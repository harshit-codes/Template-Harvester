# Unified CSV - All Platform Templates

Complete documentation for the unified CSV that combines templates from Zapier, Make.com, and n8n.

## Quick Start

### Create Unified CSV:

```bash
python create_unified_csv.py
```

This will automatically:
- Load the latest CSV files from all three platforms
- Validate and clean the data
- Remove any duplicates
- Sort by platform and popularity
- Generate comprehensive statistics
- Output a single unified CSV file

## Output

**File Location**: `./exports/unified_templates_[timestamp].csv`

**File Size**: ~43 MB

**Total Templates**: 15,011

## Dataset Composition

### By Platform:
- **Make.com**: 8,011 templates (53.4%)
- **n8n**: 6,537 templates (43.5%)
- **Zapier**: 463 templates (3.1%)

### Data Quality:
- **All templates are published**: 100%
- **Templates with creator info**: 46.6%
- **Templates with view counts**: 43.5%
- **Templates with usage counts**: 53.4%
- **Public templates**: 100%
- **Verified creators**: 5,868

## Schema

The unified CSV maintains the complete 29-field schema across all platforms:

### Core Identification
- `platform` - Source platform (zapier, make, n8n)
- `platform_id` - Unique ID format: `{platform}_{native_id}`
- `platform_native_id` - Original platform ID
- `name` - Template name
- `title` - Template title

### Description Fields
- `description` - Full description
- `description_html` - HTML formatted description
- `description_plain` - Plain text description

### URLs
- `url` - Template view URL
- `create_url` - URL to use/create from template

### Status & Visibility
- `status` - Template status (published, private, etc.)
- `is_public` - Boolean public visibility

### Categorization
- `category` - Primary category
- `tags` - Tags (semicolon/comma separated)
- `apps_used` - Apps/nodes used (comma separated)
- `nodes_used` - Number of nodes/steps

### Metrics
- `total_views` - View count
- `total_downloads` - Download count
- `usage_count` - Usage/popularity metric

### Creator Information
- `creator_name` - Creator name
- `creator_verified` - Verification status
- `creator_avatar_url` - Creator avatar URL

### Timestamps
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `published_at` - Publication timestamp
- `approved_at` - Approval timestamp
- `approval_requested` - Approval request status

### Additional Metadata
- `slug` - URL slug
- `team_id` - Team/organization ID
- `type` - Template type

## Top 20 Most Used Apps/Nodes

Across all 15,011 templates:

1. **HTTP Request**: 3,085 templates
2. **Code**: 2,761 templates
3. **AI Agent**: 2,031 templates
4. **Google Sheets**: 1,805 templates
5. **OpenAI Chat Model**: 1,514 templates
6. **google-sheets**: 1,438 templates
7. **Gmail**: 1,007 templates
8. **builtin**: 971 templates
9. **Structured Output Parser**: 906 templates
10. **OpenAI**: 848 templates
11. **Telegram**: 781 templates
12. **Google Drive**: 719 templates
13. **Simple Memory**: 662 templates
14. **Basic LLM Chain**: 610 templates
15. **Google Gemini Chat Model**: 605 templates
16. **slack**: 588 templates
17. **Slack**: 543 templates
18. **openai-gpt-3**: 428 templates
19. **airtable**: 419 templates
20. **util**: 414 templates

## Data Processing

The unification script performs these operations:

### 1. Loading
- Loads CSV files from all three platforms
- Validates each row has required fields (platform, platform_id, name, url)
- Skips invalid rows and logs warnings

### 2. Deduplication
- Checks for duplicate `platform_id` values
- Keeps first occurrence, removes duplicates
- Logs number of duplicates removed

### 3. Sorting
- Primary sort: Platform (alphabetically)
- Secondary sort: Popularity (descending)
- Popularity metric: max(total_views, usage_count)

### 4. Statistics Generation
- Counts templates by platform and status
- Calculates data coverage percentages
- Identifies most used apps/nodes
- Generates comprehensive report

## Platform-Specific Notes

### Make.com (53.4% of dataset)
- **Strengths**: Usage counts, app information
- **Data Coverage**: Good overall coverage
- **Unique Aspect**: All templates sorted by usage (most popular first)

### n8n (43.5% of dataset)
- **Strengths**: Creator info, view counts, detailed node information
- **Data Coverage**: Excellent creator and engagement metrics
- **Unique Aspect**: Rich metadata including verified creators

### Zapier (3.1% of dataset)
- **Strengths**: Template names and descriptions
- **Data Coverage**: Limited due to web scraping challenges
- **Unique Aspect**: Includes interface-only templates (forms, tables)

## Use Cases

This unified CSV is perfect for:

1. **Cross-Platform Analysis**
   - Compare template popularity across platforms
   - Identify trending apps and integrations
   - Analyze platform ecosystems

2. **Market Research**
   - Understand automation use cases
   - Identify popular integration patterns
   - Track emerging tools and services

3. **Data Science Projects**
   - Train AI models on automation patterns
   - Analyze workflow complexity
   - Study creator ecosystems

4. **Business Intelligence**
   - Competitive analysis
   - Market sizing
   - Feature gap analysis

## File Management

### Source Files Used:
- Zapier: `zapier_templates_20251028_100630_2025-10-28_10-06-30.csv`
- Make.com: `make_templates_20251028_104024_2025-10-28_10-40-24.csv`
- n8n: `n8n_templates_20251028_104701_2025-10-28_10-47-01.csv`

### To Regenerate:
Simply run the script again after fetching updated platform data:
```bash
python create_unified_csv.py
```

The script will automatically use the latest CSV files from each platform.

## Statistics Summary

```
📊 Total Templates: 15,011

📦 By Platform:
   • MAKE: 8,011 (53.4%)
   • N8N: 6,537 (43.5%)
   • ZAPIER: 463 (3.1%)

📈 Status Distribution:
   • published: 15,011 (100.0%)

📋 Data Coverage:
   • Templates with creator info: 6,998 (46.6%)
   • Templates with view counts: 6,537 (43.5%)
   • Templates with usage counts: 8,011 (53.4%)
   • Public templates: 15,011 (100.0%)
   • Verified creators: 5,868
```

## Updates and Maintenance

To update the unified CSV with fresh data:

1. Run platform-specific scrapers to get latest templates:
   ```bash
   python scrape_zapier_production.py
   python scrape_make_production.py
   python scrape_n8n_production.py
   ```

2. Create new unified CSV:
   ```bash
   python create_unified_csv.py
   ```

3. The script will automatically detect and use the latest CSV files

## Support

For questions or issues with the unified CSV:
- Check the logs during generation
- Verify source CSV files are present in `./exports/`
- Ensure source files follow the expected 29-field schema
