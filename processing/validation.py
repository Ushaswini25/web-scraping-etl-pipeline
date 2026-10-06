from urllib.parse import urlparse


REQUIRED_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
]

VALID_SOURCES = [
    "books_to_scrape",
    "quotes_to_scrape",
]


def is_valid_url(url):
    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def validate_record(record):
    errors = []

    for field in REQUIRED_FIELDS:
        value = record.get(field, "")

        if not value or not str(value).strip():
            errors.append(
                f"Missing required field: {field}"
            )

    source = record.get("source", "")

    if source not in VALID_SOURCES:
        errors.append("Invalid source")

    source_url = record.get("source_url", "")

    if not source_url:
        errors.append("Missing source_url")
    elif not is_valid_url(source_url):
        errors.append("Invalid source_url")

    price = record.get("price", "")

    if price:
        try:
            price_value = float(price)

            if price_value < 0:
                errors.append("Price cannot be negative")

        except (ValueError, TypeError):
            errors.append("Invalid price")

    rating = record.get("rating", "")

    if rating:
        if rating not in ["1", "2", "3", "4", "5"]:
            errors.append("Invalid rating")

    return errors


def is_valid_record(record):
    return len(validate_record(record)) == 0