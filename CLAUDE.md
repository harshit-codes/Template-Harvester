# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Template Harvester is a Python application that extracts automation templates from n8n, Make.com, and Zapier APIs and consolidates them into a unified CSV file. The application handles pagination, rate limiting, and normalizes disparate API responses into a standardized schema.

## Running the Application

Execute the main script from the project root:

```bash
python -m template_harvester.main
```

## Configuration

All configuration is managed via `config.json` in the root directory:

- **Platform Configuration**: Each platform (n8n, make, zapier) has its own section with `enabled` flag, `base_url`, pagination settings, and API credentials
- **Output Settings**: Control CSV filename, timestamp inclusion, and export directory (`./exports`)
- **Logging Settings**: Configure log level, file location (`./logs/scraper.log`), and console output

API keys must be added to `config.json` before running:
- Make.com: `api_key` field
- Zapier: `client_id` field (currently disabled by default)
- n8n: No authentication required (public API)

## Architecture

The codebase follows a modular three-stage pipeline pattern:

### 1. Scrapers (`template_harvester/scrapers/`)
- **BaseScraper** (base_scraper.py:6): Abstract base class providing common HTTP request functionality with retry logic, exponential backoff, and rate limit handling
- Platform-specific scrapers (N8nScraper, MakeScraper) inherit from BaseScraper and implement `fetch_templates()` to handle pagination and extract raw template data from each API

### 2. Normalizers (`template_harvester/normalizers/`)
- **BaseNormalizer** (base_normalizer.py:3): Abstract base class defining the `normalize()` interface
- Platform-specific normalizers transform raw API responses into the unified CSV schema with 26 standardized fields (defined in csv_exporter.py:25-56)

### 3. Exporters (`template_harvester/exporters/`)
- **CSVExporter** (csv_exporter.py:6): Handles writing normalized data to timestamped CSV files with the unified schema

### Main Orchestration

The `main()` function (main.py:18) coordinates the pipeline:
1. Loads configuration
2. Instantiates scrapers and normalizers for enabled platforms
3. Fetches and normalizes templates from each platform sequentially with 1-second delays
4. Sorts combined results by platform and name
5. Exports to CSV with summary statistics

## Adding Support for New Platforms

To add a new platform:
1. Create a scraper in `scrapers/` inheriting from BaseScraper
2. Create a normalizer in `normalizers/` inheriting from BaseNormalizer
3. Add platform configuration to `config.json`
4. Register both in `main.py` scrapers and normalizers dictionaries

## Unified CSV Schema

The normalized schema includes 26 fields covering:
- Platform metadata (platform, platform_id, platform_native_id)
- Template info (name, title, description variants, urls)
- Visibility and status (status, is_public, approval states)
- Classification (category, tags, apps_used, nodes_used)
- Metrics (total_views, total_downloads, usage_count)
- Creator info (creator_name, creator_verified, creator_avatar_url)
- Timestamps (created_at, updated_at, published_at, approved_at)

All normalizers must map their platform's data to these fields, using None/empty values where data is unavailable.
