#!/usr/bin/env python
"""
Production-ready Make.com template scraper using API
- API-based retrieval (fast and reliable)
- Rate limiting and respectful API usage
- Retry logic with exponential backoff
- Progress tracking
- Error recovery and logging
- Incremental CSV writing
"""
import logging
import time
import sys
import signal
from datetime import datetime
from template_harvester.config import load_config
from template_harvester.utils.logging_setup import setup_logging
from template_harvester.scrapers.make_scraper import MakeScraper
from template_harvester.normalizers.make_normalizer import MakeNormalizer
from template_harvester.exporters.csv_exporter import CSVExporter


class GracefulKiller:
    """Handle keyboard interrupts gracefully"""
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        logging.warning("\n\n⚠️  Interrupt received. Finishing current batch and saving progress...")
        self.kill_now = True


def main():
    # Initialize graceful shutdown handler
    killer = GracefulKiller()

    # Load config
    config = load_config()
    setup_logging(config)

    # Print banner
    logging.info("=" * 80)
    logging.info("  MAKE.COM TEMPLATE SCRAPER - PRODUCTION MODE")
    logging.info("=" * 80)
    logging.info("")
    logging.info("Configuration:")

    scraper_config = config['platforms']['make']
    logging.info(f"  • Base URL: {scraper_config.get('base_url')}")
    logging.info(f"  • API endpoint: /api/v2/templates/public")
    logging.info(f"  • Batch size: {scraper_config.get('limit', 100)} templates per request")
    logging.info(f"  • Max pages: {scraper_config.get('max_pages', 10)}")
    logging.info(f"  • Incremental CSV writing: Enabled")
    logging.info(f"  • Keyboard interrupt: Graceful shutdown enabled")
    logging.info("")

    # Initialize components
    scraper = MakeScraper(scraper_config)
    normalizer = MakeNormalizer()
    exporter = CSVExporter(config)

    # Track statistics
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'start_time': time.time()
    }

    try:
        # Start CSV export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = exporter.start_export(f'make_templates_{timestamp}')
        logging.info(f"📄 CSV file: {filepath}")
        logging.info("")
        logging.info("=" * 80)
        logging.info("  STARTING SCRAPE")
        logging.info("=" * 80)
        logging.info("")

        # Fetch all templates via API
        logging.info("📥 Fetching templates from Make.com API...")

        try:
            # Fetch all templates
            templates = scraper.fetch_templates()

            if not templates:
                logging.error("❌ No templates found. Exiting.")
                return 1

            stats['total'] = len(templates)
            logging.info(f"✅ Retrieved {stats['total']} templates from Make.com API")
            logging.info("")
            logging.info("=" * 80)
            logging.info("  NORMALIZING AND WRITING TO CSV")
            logging.info("=" * 80)
            logging.info("")

            # Process and write each template
            for i, template_data in enumerate(templates, 1):
                # Check for interrupt
                if killer.kill_now:
                    logging.warning("⚠️  Gracefully stopping scraper...")
                    break

                try:
                    template_id = template_data.get('id')
                    name = template_data.get('name', 'Unknown')

                    logging.info(f"[{i}/{stats['total']}] ID: {template_id}")
                    logging.info(f"  📝 {name[:60]}")

                    # Show extracted info
                    apps = template_data.get('usedApps', [])
                    usage = template_data.get('usage', 0)
                    logging.info(f"  🔗 Apps: {', '.join(apps[:5])}{' ...' if len(apps) > 5 else ''}")
                    logging.info(f"  📊 Usage: {usage:,}")

                    # Normalize
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

                    # Progress update every 50 templates
                    if i % 50 == 0:
                        elapsed = time.time() - stats['start_time']
                        avg_time = elapsed / i
                        remaining = (stats['total'] - i) * avg_time
                        success_rate = (stats['success'] / i * 100) if i > 0 else 0

                        logging.info("")
                        logging.info(f"{'─' * 80}")
                        logging.info(f"  📊 PROGRESS: {i}/{stats['total']} ({i / stats['total'] * 100:.1f}%)")
                        logging.info(f"  ✅ Success: {stats['success']} | ❌ Failed: {stats['failed']} | Rate: {success_rate:.1f}%")
                        logging.info(f"  ⏱️  Avg: {avg_time:.2f}s/template | Remaining: {remaining:.1f}s")
                        logging.info(f"{'─' * 80}")
                        logging.info("")

                except Exception as e:
                    stats['failed'] += 1
                    logging.error(f"  ✗ Error processing template: {e}")
                    continue

        except Exception as e:
            logging.error(f"❌ Error fetching templates from API: {e}")
            import traceback
            traceback.print_exc()
            return 1

        # Close CSV file
        final_path = exporter.close()

        # Final statistics
        elapsed_total = time.time() - stats['start_time']

        logging.info("")
        logging.info("=" * 80)
        logging.info("  SCRAPING COMPLETE")
        logging.info("=" * 80)
        logging.info("")
        logging.info(f"📊 Final Statistics:")
        logging.info(f"  • Total templates: {stats['total']}")
        logging.info(f"  • Successfully processed: {stats['success']}")
        logging.info(f"  • Failed: {stats['failed']}")
        logging.info(f"  • Success rate: {(stats['success'] / stats['total'] * 100):.1f}%" if stats['total'] > 0 else "  • Success rate: N/A")
        logging.info("")
        logging.info(f"⏱️  Time:")
        logging.info(f"  • Total: {elapsed_total:.2f} seconds ({elapsed_total / 60:.2f} minutes)")
        logging.info(f"  • Average: {elapsed_total / stats['total']:.2f}s per template" if stats['total'] > 0 else "  • Average: N/A")
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


if __name__ == "__main__":
    sys.exit(main())
