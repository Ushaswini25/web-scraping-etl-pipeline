# AI Usage

## Purpose

AI assistance was used during the development of this web scraping ETL assignment to understand the implementation approach and improve code structure.

## Areas Where AI Assistance Was Used

AI assistance was used for:

- Understanding the project structure.
- Understanding HTML elements and CSS selectors.
- Designing the base scraper.
- Implementing HTTP requests and retry handling.
- Implementing dynamic pagination.
- Creating cleaning functions.
- Designing validation rules.
- Implementing duplicate detection using fingerprints.
- Creating unit tests.
- Structuring the main ETL pipeline.
- Improving README documentation.

## Human Understanding and Verification

The generated code was reviewed and tested manually.

The following were verified:

- The scraper successfully connects to both websites.
- Pagination is followed dynamically.
- Scraped records are converted to the common schema.
- Cleaning functions produce normalized values.
- Invalid records are rejected without crashing the program.
- Duplicate detection works with case, spacing, and punctuation differences.
- Unit tests are executed using pytest.
- CSV and JSON output files are generated.
- The reconciliation calculation is checked in the summary report.

## Limitations

AI-generated suggestions were treated as development assistance rather than as an automatic solution. The code was reviewed, modified where necessary, and tested before use.