# Make.com Template Scraper

Production-ready API scraper for extracting all Make.com public templates to CSV.

## Quick Start

### Prerequisites

1. Make sure the API key is saved in the `.env` file:
   ```
   MAKE_API_KEY=your-api-key-here
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Single Command to Run:

```bash
python scrape_make_production.py
```

That's it! The script will:
- Fetch all public Make.com templates via API
- Write each template to CSV immediately (incremental writing)
- Save to `./exports/make_templates_[timestamp].csv`
- Complete in seconds (API-based, very fast!)

## Features & Guardrails

✅ **API-Based Retrieval**
- Uses official Make.com public templates API
- Fast and reliable data extraction
- No web scraping needed

✅ **Error Recovery**
- Automatic retry with exponential backoff (via BaseScraper)
- Validates data before writing
- Continues on errors, tracks failures

✅ **Progress Tracking**
- Real-time progress updates every 50 templates
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

The CSV includes these fields for each template:

**Core Info:**
- Platform (make)
- Platform ID and native ID
- Template name and title
- Description
- URL and slug
- Status (all public templates are "published")

**Apps:**
- Apps used (comma-separated list)
- Usage count

**Metadata:**
- All templates from public API are marked as public
- Type: template

**Note:** The public API provides limited fields compared to private templates API. The following fields are not available:
- Creator information
- Timestamps (created, updated, published)
- Category and tags
- Views and downloads (only usage count is available)
- Team information
- Approval data

## API Endpoint

The scraper uses Make.com's public templates endpoint:
- **URL:** `https://eu1.make.com/api/v2/templates/public`
- **Authentication:** Token-based (from .env file)
- **Pagination:** Supports offset and limit parameters
- **Sorting:** By usage (descending) for most popular templates first

## Configuration

Edit `config.json` to adjust settings:

```json
{
  "make": {
    "enabled": true,
    "base_url": "https://eu1.make.com",
    "max_pages": 10,          // Maximum pages to fetch (safety limit)
    "limit": 100              // Templates per API request (max: 100)
  }
}
```

## Testing

The scraper will fetch all available public templates. Based on the API response:
- Sorted by usage (most popular first)
- Typically hundreds to thousands of templates
- Very fast (API-based, no page rendering needed)

## Expected Runtime

- **API-based retrieval**: Usually completes in seconds to minutes
- **Much faster than web scraping** (no page loads, no scrolling)
- **Success rate**: Typically 100% (API is reliable)

## Output Location

- **CSV file**: `./exports/make_templates_[timestamp].csv`
- **Log file**: `./logs/scraper.log`

## Notes

- The scraper uses the **public templates API**, which provides less data than the private templates API
- All templates are public and published (that's what the public API returns)
- The API returns templates sorted by usage count (most popular first)
- No rate limiting needed for normal API usage (respectful by design)

## Troubleshooting

**"MAKE_API_KEY not found in .env file"**
- Ensure you have created a `.env` file in the project root
- Add your Make.com API key: `MAKE_API_KEY=your-key-here`

**"Organization not found" error**
- This happens when using the wrong endpoint (e.g., `/api/v2/templates` instead of `/api/v2/templates/public`)
- The scraper uses the correct public endpoint

**"No templates found"**
- Check your internet connection
- Verify the API key is valid
- Check the logs at `./logs/scraper.log` for detailed error messages

**Script interrupted**
- Press Ctrl+C once for graceful shutdown
- CSV file will be saved with templates processed so far
- Logs show progress in `./logs/scraper.log`

## API Response Structure

The Make.com public templates API returns:

```json
{
  "templatesPublic": [
    {
      "id": 12593,
      "name": "Template Name",
      "description": "Template description with optional markdown",
      "url": "template-slug",
      "usedApps": ["app1", "app2"],
      "usage": 12345
    }
  ],
  "pg": {
    "sortBy": "usage",
    "limit": 100,
    "sortDir": "desc",
    "offset": 0
  }
}
```

## Support

For issues or questions, check the logs at `./logs/scraper.log`
