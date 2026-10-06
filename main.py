import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import remove_duplicates


BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


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


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def scrape_data():
    logger.info("Starting scraping process")

    books_scraper = BooksScraper()
    quotes_scraper = QuotesScraper()

    books = []
    quotes = []

    try:
        books = books_scraper.scrape()
    except Exception as exc:
        logger.exception(
            "Books scraper failed: %s",
            exc
        )

    try:
        quotes = quotes_scraper.scrape()
    except Exception as exc:
        logger.exception(
            "Quotes scraper failed: %s",
            exc
        )

    logger.info(
        "Books scraped: %d",
        len(books)
    )

    logger.info(
        "Quotes scraped: %d",
        len(quotes)
    )

    return books + quotes


def clean_and_validate(records):
    valid_records = []
    rejected_records = []

    for record in records:
        cleaned_record = clean_record(record)

        errors = validate_record(cleaned_record)

        if errors:
            rejected_records.append({
                "record": cleaned_record,
                "errors": errors,
            })

            logger.warning(
                "Rejected record: %s | Errors: %s",
                cleaned_record.get(
                    "name_or_title",
                    ""
                ),
                errors,
            )

            continue

        cleaned_record["scraped_at"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        valid_records.append(cleaned_record)

    return (
        valid_records,
        rejected_records
    )


def save_csv(records):
    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()
        writer.writerows(records)

    logger.info(
        "Final CSV saved: %s",
        CSV_FILE
    )


def count_by_source(records):
    counts = {
        "books_to_scrape": 0,
        "quotes_to_scrape": 0,
    }

    for record in records:
        source = record.get("source", "")

        if source in counts:
            counts[source] += 1

    return counts


def save_summary(
    raw_records,
    cleaned_records,
    rejected_records,
    duplicate_count,
    final_records,
    execution_time_seconds,
):
    raw_counts = count_by_source(raw_records)

    cleaned_counts = count_by_source(cleaned_records)

    final_counts = count_by_source(final_records)

    summary = {
        "run_timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),

        "execution_time_seconds": (
            execution_time_seconds
        ),

        "records_collected_per_source": raw_counts,

        "raw_records": len(raw_records),

        "records_after_cleaning_and_validation": (
            len(cleaned_records)
        ),

        "records_after_cleaning_and_validation_per_source": (
            cleaned_counts
        ),

        "rejected_records": len(rejected_records),

        "duplicate_records": duplicate_count,

        "final_records": len(final_records),

        "final_records_per_source": final_counts,

        "reconciliation": (
            len(raw_records)
            - len(rejected_records)
            - duplicate_count
            == len(final_records)
        ),

        "rejected_details": rejected_records,
    }

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        "Summary report saved: %s",
        JSON_FILE
    )


def main():
    start_time = time.perf_counter()

    logger.info(
        "========== SCRAPING STARTED =========="
    )

    raw_records = scrape_data()

    print(
        "Raw records:",
        len(raw_records)
    )

    cleaned_records, rejected_records = (
        clean_and_validate(raw_records)
    )

    print(
        "Records after cleaning and validation:",
        len(cleaned_records)
    )

    print(
        "Rejected records:",
        len(rejected_records)
    )

    unique_records, duplicate_count = (
        remove_duplicates(cleaned_records)
    )

    print(
        "Duplicate records:",
        duplicate_count
    )

    print(
        "Final records:",
        len(unique_records)
    )

    save_csv(unique_records)

    execution_time_seconds = round(
        time.perf_counter() - start_time,
        2
    )

    save_summary(
        raw_records=raw_records,
        cleaned_records=cleaned_records,
        rejected_records=rejected_records,
        duplicate_count=duplicate_count,
        final_records=unique_records,
        execution_time_seconds=execution_time_seconds,
    )

    logger.info(
        "Execution time: %.2f seconds",
        execution_time_seconds
    )

    logger.info(
        "========== SCRAPING COMPLETED =========="
    )

    print(
        "\nExecution time:",
        execution_time_seconds,
        "seconds"
    )

    print("\nFiles generated:")
    print(CSV_FILE)
    print(JSON_FILE)
    print(LOG_FILE)


if __name__ == "__main__":
    main()