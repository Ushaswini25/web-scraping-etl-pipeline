from urllib.parse import urlparse


REQUIRED_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
]


def is_valid_url(url):
    try:
        parsed = urlparse(url)

        return parsed.scheme in ("http", "https") and bool(parsed.netloc)

    except Exception:
        return False


def validate_record(record):
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field, "")

        if not value or not str(value).strip():
            errors.append(f"Missing required field: {field}")

    # Validate source
    if record.get("source") not in [
        "books_to_scrape",
        "quotes_to_scrape",
    ]:
        errors.append("Invalid source")

    # Validate URL
    source_url = record.get("source_url", "")

    if source_url and not is_valid_url(source_url):
        errors.append("Invalid source_url")

    # Validate price
    price = record.get("price", "")

    if price:
        try:
            float(price)
        except (ValueError, TypeError):
            errors.append("Invalid price")

    # Validate rating
    rating = record.get("rating", "")

    if rating:
        if rating not in ["1", "2", "3", "4", "5"]:
            errors.append("Invalid rating")

    return errors


def is_valid_record(record):
    return len(validate_record(record)) == 0