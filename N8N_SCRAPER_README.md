# n8n Template Scraper

Production-ready API scraper for extracting all n8n workflow templates to CSV.

## Quick Start

### Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

### Single Command to Run:

```bash
python scrape_n8n_production.py
```

That's it! The script will:
- Fetch all public n8n workflow templates via API (~6,500+ templates)
- Write each template to CSV immediately (incremental writing)
- Save to `./exports/n8n_templates_[timestamp].csv`
- Complete in minutes (API-based, very fast!)

## Features & Guardrails

✅ **API-Based Retrieval**
- Uses official n8n public templates API
- Fast and reliable data extraction
- No web scraping needed

✅ **Error Recovery**
- Automatic retry with exponential backoff (via BaseScraper)
- Validates data before writing
- Continues on errors, tracks failures

✅ **Progress Tracking**
- Real-time progress updates every 100 templates
- Success/failure statistics
- Time estimates and completion ETA

✅ **Graceful Shutdown**
- Press Ctrl+C to stop gracefully
- Finishes current template before stopping
- CSV file is properly closed and saved

✅ **Incremental Writing**
- Each template written to CSV immediately
- No data loss if interrupted
- Memory efficient (doesn't store all data in RAM)

## Output

The CSV includes these fields for each workflow template:

**Core Info:**
- Platform (n8n)
- Platform ID and native ID
- Workflow name and title
- Description
- URL (format: https://n8n.io/workflows/{id}/)
- Status (all public workflows are "published")

**Creator Information:**
- Creator name
- Creator username (stored in slug field)
- Creator verified status
- Creator avatar URL

**Workflow Details:**
- Apps/nodes used (comma-separated display names)
- Number of nodes
- Total views

**Metadata:**
- Created timestamp
- All workflows from public API are marked as public
- Type: workflow

**Note:** The public API provides rich data including creator information and view counts. However, some fields like categories, tags, downloads, and update timestamps are not available through the public API.

## API Endpoint

The scraper uses n8n's public templates search endpoint:
- **URL:** `https://api.n8n.io/templates/search`
- **Authentication:** None required (public API)
- **Pagination:** Supports page and rows parameters
- **Total Available:** ~6,541 workflow templates (as of current count)

## Configuration

Edit `config.json` to adjust settings:

```json
{
  "n8n": {
    "enabled": true,
    "base_url": "https://api.n8n.io",
    "max_pages": 100,         // Maximum pages to fetch (safety limit)
    "rows_per_page": 100      // Templates per API request (max: 100)
  }
}
```

## Testing

The scraper will fetch all available public workflow templates. Based on the API:
- Total workflows available: ~6,541 (and growing)
- Sorted by various criteria (configurable via API)
- Very fast (API-based, no page rendering needed)
- Includes rich metadata (creator info, view counts, node details)

## Expected Runtime

- **API-based retrieval**: Usually completes in a few minutes
- **Much faster than web scraping** (no page loads, no scrolling)
- **Success rate**: Typically 100% (API is reliable)
- **Average**: <0.1s per workflow when API is responsive

## Output Location

- **CSV file**: `./exports/n8n_templates_[timestamp].csv`
- **Log file**: `./logs/scraper.log`

## Notes

- The scraper uses the **public templates API**, which provides excellent data coverage
- All workflows are public and published (that's what the public API returns)
- Rich creator information is available (name, username, verified status, avatar)
- Node/app information is extracted from the detailed node array
- No authentication required for the public API
- No rate limiting needed for normal API usage (respectful by design)

## Troubleshooting

**"No templates found"**
- Check your internet connection
- Verify n8n API is accessible: https://api.n8n.io/templates/search
- Check the logs at `./logs/scraper.log` for detailed error messages

**Slow response times**
- The n8n API is generally very fast
- If experiencing slowness, check your network connection
- Consider reducing `rows_per_page` if encountering timeouts

**Script interrupted**
- Press Ctrl+C once for graceful shutdown
- CSV file will be saved with workflows processed so far
- Logs show progress in `./logs/scraper.log`

## API Response Structure

The n8n public templates API returns:

```json
{
  "totalWorkflows": 6541,
  "workflows": [
    {
      "id": 6270,
      "name": "Build Your First AI Agent",
      "totalViews": 99862,
      "purchaseUrl": null,
      "user": {
        "id": 91332,
        "name": "Lucas Peyrin",
        "username": "lucaspeyrin",
        "verified": true,
        "avatar": "https://gravatar.com/..."
      },
      "description": "How it works...",
      "createdAt": "2025-07-22T12:14:21.343Z",
      "nodes": [
        {
          "id": 1119,
          "name": "@n8n/n8n-nodes-langchain.agent",
          "displayName": "AI Agent",
          ...
        }
      ]
    }
  ],
  "filters": [...]
}
```

## Workflow Categories

Based on the API filters, popular workflow categories include:
- AI (4,269 workflows)
- Multimodal AI (2,393 workflows)
- Marketing (1,946 workflows)
- AI Summarization (1,124 workflows)
- Content Creation (1,049 workflows)
- IT Ops (818 workflows)
- Sales (813 workflows)
- AI Chatbot (705 workflows)
- Document Ops (641 workflows)

## Popular Nodes/Apps

Most commonly used nodes in workflows:
- Sticky Note
- Edit Fields (Set)
- HTTP Request
- Code
- If
- AI Agent
- Google Sheets
- OpenAI Chat Model
- Schedule
- Manual

## Support

For issues or questions, check the logs at `./logs/scraper.log`
