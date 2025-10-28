# Zapier Template Scraper

Production-ready scraper for extracting all Zapier templates to CSV.

## Quick Start

### Single Command to Run:

```bash
python scrape_zapier_production.py
```

That's it! The script will:
- Scrape all ~463 Zapier templates
- Write each template to CSV immediately (incremental writing)
- Save to `./exports/zapier_templates_[timestamp].csv`
- Take approximately 1-1.5 hours to complete

## Features & Guardrails

✅ **Rate Limiting**
- 3 second delay between requests
- 10 second batch pause every 50 templates
- Respectful to Zapier's servers

✅ **Error Recovery**
- Automatic retry with exponential backoff (up to 3 attempts)
- Validates data before writing
- Continues on errors, tracks failures

✅ **Progress Tracking**
- Real-time progress updates every 10 templates
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
- Platform (zapier)
- Template name, title, description
- URL and slug
- Status (published/featured)

**Categorization:**
- Category
- Tags
- Apps used (if applicable)
- Template type

**Metadata:**
- Platform ID
- Creator information
- Dates (created, updated, published)

**Assets:**
- Number of Zaps, Tables, Interfaces, Canvases

## Configuration

Edit `config.json` to adjust settings:

```json
{
  "zapier": {
    "max_templates": null,      // Set to number for testing (e.g., 10)
    "rate_limit_delay": 3,       // Seconds between requests
    "max_retries": 3,            // Retry attempts per template
    "retry_delay": 5,            // Base retry delay (exponential backoff)
    "batch_delay": 10,           // Pause every batch_size templates
    "batch_size": 50             // Templates per batch
  }
}
```

## Testing

To test with only 10 templates:

1. Edit `config.json`: Set `"max_templates": 10`
2. Run: `python scrape_zapier_production.py`
3. Set back to `null` for full scrape

## Expected Runtime

- **Full scrape (463 templates)**: ~1-1.5 hours
- **Average per template**: ~11-15 seconds
- **Success rate**: Typically 95-100%

## Output Location

- **CSV file**: `./exports/zapier_templates_[timestamp].csv`
- **Log file**: `./logs/scraper.log`

## Notes

- Many Zapier templates are "Interface-only" (forms/tables) without traditional app workflows
- Missing "apps_used" is expected for Interface-only templates
- The scraper uses Selenium with headless Chrome (auto-installs)
- Chrome/Chromium must be installed on your system

## Troubleshooting

**"No templates found"**
- Check your internet connection
- Verify Zapier's templates page is accessible

**"ChromeDriver error"**
- Ensure Chrome browser is installed
- The script auto-downloads ChromeDriver

**Script interrupted**
- Press Ctrl+C once for graceful shutdown
- CSV file will be saved with templates scraped so far
- Logs show progress in `./logs/scraper.log`

## Support

For issues or questions, check the logs at `./logs/scraper.log`
