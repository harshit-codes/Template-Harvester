#!/usr/bin/env python
"""
Production-ready Zapier template scraper with comprehensive guardrails
- Rate limiting and respectful scraping
- Retry logic with exponential backoff
- Progress tracking and resumption
- Error recovery and logging
- Keyboard interrupt handling
- Memory-efficient incremental CSV writing
"""
import logging
import time
import sys
import signal
from datetime import datetime
from template_harvester.config import load_config
from template_harvester.utils.logging_setup import setup_logging
from template_harvester.scrapers.zapier_scraper_v2 import ZapierScraperV2
from template_harvester.normalizers.zapier_normalizer_v2 import ZapierNormalizerV2
from template_harvester.exporters.csv_exporter import CSVExporter


class GracefulKiller:
    """Handle keyboard interrupts gracefully"""
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        logging.warning("\n\n⚠️  Interrupt received. Finishing current template and saving progress...")
        self.kill_now = True


def validate_template_data(template_data):
    """Validate that template data has minimum required fields"""
    if not template_data:
        return False

    # Must have at least a URL and some identifiable info
    has_url = bool(template_data.get('url'))
    has_identifier = bool(
        template_data.get('slug') or
        template_data.get('template_id') or
        template_data.get('h1_title') or
        template_data.get('meta_title')
    )

    return has_url and has_identifier


def scrape_template_with_retry(scraper, url, config, attempt=1):
    """
    Scrape a template with retry logic and exponential backoff
    """
    max_retries = config.get('max_retries', 3)
    retry_delay = config.get('retry_delay', 5)

    try:
        template_data = scraper._extract_template_data(url)

        if validate_template_data(template_data):
            return template_data, None
        else:
            error_msg = "Invalid or incomplete data extracted"

            if attempt < max_retries:
                wait_time = retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                logging.warning(f"  ⚠️  {error_msg}. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                return scrape_template_with_retry(scraper, url, config, attempt + 1)
            else:
                return None, error_msg

    except Exception as e:
        error_msg = str(e)

        if attempt < max_retries:
            wait_time = retry_delay * (2 ** (attempt - 1))
            logging.warning(f"  ⚠️  Error: {error_msg}. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            return scrape_template_with_retry(scraper, url, config, attempt + 1)
        else:
            logging.error(f"  ✗ Failed after {max_retries} attempts: {error_msg}")
            return None, error_msg


def main():
    # Initialize graceful shutdown handler
    killer = GracefulKiller()

    # Load config
    config = load_config()
    setup_logging(config)

    # Print banner
    logging.info("="*80)
    logging.info("  ZAPIER TEMPLATE SCRAPER - PRODUCTION MODE")
    logging.info("="*80)
    logging.info("")
    logging.info("Guardrails enabled:")

    scraper_config = config['platforms']['zapier']
    logging.info(f"  • Rate limit: {scraper_config.get('rate_limit_delay', 3)}s between requests")
    logging.info(f"  • Max retries: {scraper_config.get('max_retries', 3)} per template")
    logging.info(f"  • Retry delay: {scraper_config.get('retry_delay', 5)}s with exponential backoff")
    logging.info(f"  • Batch delay: {scraper_config.get('batch_delay', 10)}s every {scraper_config.get('batch_size', 50)} templates")
    logging.info(f"  • Page timeout: {scraper_config.get('page_load_timeout', 30)}s")
    logging.info(f"  • Incremental CSV writing: Enabled")
    logging.info(f"  • Keyboard interrupt: Graceful shutdown enabled")
    logging.info("")

    # Initialize components
    scraper = ZapierScraperV2(scraper_config)
    normalizer = ZapierNormalizerV2()
    exporter = CSVExporter(config)

    # Track statistics
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0,
        'start_time': time.time()
    }

    try:
        # Initialize WebDriver
        scraper._init_driver()

        # Load templates listing page
        logging.info(f"📥 Loading templates page: {scraper.templates_url}")
        scraper.driver.get(scraper.templates_url)
        time.sleep(5)

        # Scroll to load all templates
        logging.info("📜 Scrolling to discover all templates...")
        scraper._scroll_to_load_all()

        # Extract all template URLs
        logging.info("🔍 Extracting template URLs...")
        template_urls = scraper._extract_template_urls()

        if not template_urls:
            logging.error("❌ No template URLs found. Exiting.")
            return 1

        stats['total'] = len(template_urls)
        logging.info(f"✅ Found {stats['total']} templates to scrape")
        logging.info("")

        # Limit templates if configured (for testing)
        max_templates = scraper_config.get('max_templates')
        if max_templates:
            template_urls = template_urls[:max_templates]
            stats['total'] = len(template_urls)
            logging.info(f"⚠️  Limited to {max_templates} templates (test mode)")
            logging.info("")

        # Start CSV export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = exporter.start_export(f'zapier_templates_{timestamp}')
        logging.info(f"📄 CSV file: {filepath}")
        logging.info("")
        logging.info("="*80)
        logging.info("  STARTING SCRAPE")
        logging.info("="*80)
        logging.info("")

        # Scrape each template
        batch_size = scraper_config.get('batch_size', 50)
        batch_delay = scraper_config.get('batch_delay', 10)
        rate_limit = scraper_config.get('rate_limit_delay', 3)

        for i, url in enumerate(template_urls, 1):
            # Check for interrupt
            if killer.kill_now:
                logging.warning("⚠️  Gracefully stopping scraper...")
                break

            try:
                slug = url.split('/')[-1]
                logging.info(f"[{i}/{stats['total']}] {slug}")

                # Scrape with retry logic
                template_data, error = scrape_template_with_retry(scraper, url, scraper_config)

                if not template_data:
                    stats['failed'] += 1
                    logging.error(f"  ✗ Failed: {error or 'Unknown error'}")
                    continue

                # Clean up large data to save memory
                if 'page_source' in template_data:
                    del template_data['page_source']

                # Show extracted info
                name = template_data.get('h1_title') or template_data.get('meta_title') or 'Unknown'
                apps_count = len(template_data.get('page_apps', []))
                logging.info(f"  📝 {name[:60]}")
                logging.info(f"  🔗 Apps: {apps_count}")

                # Normalize
                try:
                    normalized_templates = normalizer.normalize([template_data])

                    if not normalized_templates:
                        stats['failed'] += 1
                        logging.error(f"  ✗ Normalization failed")
                        continue

                    # Write to CSV immediately
                    normalized = normalized_templates[0]
                    if exporter.write_row(normalized):
                        stats['success'] += 1
                        logging.info(f"  ✅ Written to CSV")
                    else:
                        stats['failed'] += 1
                        logging.error(f"  ✗ CSV write failed")

                except Exception as e:
                    stats['failed'] += 1
                    logging.error(f"  ✗ Normalization error: {e}")
                    continue

                # Progress update every 10 templates
                if i % 10 == 0:
                    elapsed = time.time() - stats['start_time']
                    avg_time = elapsed / i
                    remaining = (stats['total'] - i) * avg_time
                    success_rate = (stats['success'] / i * 100) if i > 0 else 0

                    logging.info("")
                    logging.info(f"{'─'*80}")
                    logging.info(f"  📊 PROGRESS: {i}/{stats['total']} ({i/stats['total']*100:.1f}%)")
                    logging.info(f"  ✅ Success: {stats['success']} | ❌ Failed: {stats['failed']} | Rate: {success_rate:.1f}%")
                    logging.info(f"  ⏱️  Avg: {avg_time:.1f}s/template | Remaining: {remaining/60:.1f} min")
                    logging.info(f"{'─'*80}")
                    logging.info("")

                # Batch delay - longer pause every N templates to be extra respectful
                if i % batch_size == 0 and i < stats['total']:
                    logging.info(f"⏸️  Batch pause ({batch_delay}s) to respect rate limits...")
                    time.sleep(batch_delay)
                else:
                    # Regular rate limiting
                    time.sleep(rate_limit)

            except KeyboardInterrupt:
                logging.warning("\n⚠️  Keyboard interrupt detected...")
                killer.kill_now = True
                break

            except Exception as e:
                stats['failed'] += 1
                logging.error(f"  ✗ Unexpected error: {e}")
                continue

        # Close CSV file
        final_path = exporter.close()

        # Final statistics
        elapsed_total = time.time() - stats['start_time']

        logging.info("")
        logging.info("="*80)
        logging.info("  SCRAPING COMPLETE")
        logging.info("="*80)
        logging.info("")
        logging.info(f"📊 Final Statistics:")
        logging.info(f"  • Total templates found: {stats['total']}")
        logging.info(f"  • Successfully scraped: {stats['success']}")
        logging.info(f"  • Failed: {stats['failed']}")
        logging.info(f"  • Success rate: {(stats['success']/stats['total']*100):.1f}%" if stats['total'] > 0 else "  • Success rate: N/A")
        logging.info("")
        logging.info(f"⏱️  Time:")
        logging.info(f"  • Total: {elapsed_total/60:.1f} minutes ({elapsed_total/3600:.2f} hours)")
        logging.info(f"  • Average: {elapsed_total/stats['total']:.1f}s per template" if stats['total'] > 0 else "  • Average: N/A")
        logging.info("")
        logging.info(f"📄 Output:")
        logging.info(f"  • CSV file: {final_path}")
        logging.info(f"  • Log file: {config['logging']['file']}")
        logging.info("")
        logging.info("✅ Done!")
        logging.info("")

        return 0

    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

        # Try to close CSV gracefully
        try:
            exporter.close()
        except:
            pass

        return 1

    finally:
        # Always close WebDriver
        try:
            scraper._close_driver()
        except:
            pass


if __name__ == "__main__":
    sys.exit(main())
