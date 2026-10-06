import csv
import json
import logging
from datetime import datetime
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import remove_duplicates


# Project folders
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# Output files
CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


# CSV columns
FIELDNAMES = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def scrape_data():
    """Scrape records from both websites."""

    logger.info("Starting scraping process")

    books_scraper = BooksScraper()
    quotes_scraper = QuotesScraper()

    books = books_scraper.scrape()
    quotes = quotes_scraper.scrape()

    logger.info("Books scraped: %d", len(books))
    logger.info("Quotes scraped: %d", len(quotes))

    return books + quotes


def clean_and_validate(records):
    """Clean records and reject invalid records."""

    valid_records = []
    rejected_count = 0
    rejected_records = []

    for record in records:
        cleaned_record = clean_record(record)

        errors = validate_record(cleaned_record)

        if errors:
            rejected_count += 1

            rejected_records.append({
                "record": cleaned_record,
                "errors": errors,
            })

            logger.warning(
                "Rejected record: %s | Errors: %s",
                cleaned_record.get("name_or_title", ""),
                errors,
            )

            continue

        cleaned_record["scraped_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        valid_records.append(cleaned_record)

    return valid_records, rejected_count, rejected_records


def save_csv(records):
    """Save final records to CSV."""

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(records)

    logger.info(
        "Final CSV saved: %s",
        CSV_FILE,
    )


def save_summary(
    raw_count,
    rejected_count,
    duplicate_count,
    final_count,
    rejected_records,
):
    """Save summary report as JSON."""

    summary = {
        "run_timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "raw_records": raw_count,
        "rejected_records": rejected_count,
        "duplicate_records": duplicate_count,
        "final_records": final_count,
        "reconciliation": (
            raw_count
            - rejected_count
            - duplicate_count
            == final_count
        ),
        "rejected_details": rejected_records,
    }

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False,
        )

    logger.info(
        "Summary report saved: %s",
        JSON_FILE,
    )


def main():
    """Run the complete ETL pipeline."""

    logger.info("========== SCRAPING STARTED ==========")

    # 1. Scrape
    raw_records = scrape_data()
    raw_count = len(raw_records)

    print("Raw records:", raw_count)

    # 2. Clean and validate
    valid_records, rejected_count, rejected_records = (
        clean_and_validate(raw_records)
    )

    print("Rejected records:", rejected_count)

    # 3. Remove duplicates
    unique_records, duplicate_count = remove_duplicates(
        valid_records
    )

    print("Duplicate records:", duplicate_count)
    print("Final records:", len(unique_records))

    # 4. Save CSV
    save_csv(unique_records)

    # 5. Save JSON summary
    save_summary(
        raw_count,
        rejected_count,
        duplicate_count,
        len(unique_records),
        rejected_records,
    )

    logger.info("========== SCRAPING COMPLETED ==========")

    print("\nFiles generated:")
    print(CSV_FILE)
    print(JSON_FILE)
    print(LOG_FILE)


if __name__ == "__main__":
    main()