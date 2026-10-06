# Web Scraping ETL Assignment

## Overview

This project is a Python-based web scraping and ETL pipeline that collects data from:

- Books to Scrape
- Quotes to Scrape

The scraped data is cleaned, validated, deduplicated, and stored in a common CSV format.

## Features

- Scrapes books dynamically from Books to Scrape.
- Scrapes quotes dynamically from Quotes to Scrape.
- Follows pagination using the `Next` link.
- Uses HTTP retries and request timeout handling.
- Waits between requests to avoid sending requests too quickly.
- Cleans text, prices, ratings, and tags.
- Validates scraped records.
- Rejects invalid records without stopping the program.
- Detects duplicate records using normalized fingerprints.
- Generates a final CSV dataset.
- Generates a JSON summary report.
- Maintains a scraping log.
- Includes unit tests for cleaning, validation, and deduplication.

## Project Structure

```text
scraping_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
├── logs/
│   └── scraper.log
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md