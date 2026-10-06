import hashlib
import re


def normalize_for_fingerprint(value):
    if value is None:
        return ""

    value = str(value).lower()

    # Remove punctuation and special characters
    value = re.sub(r"[^a-z0-9\s]", "", value)

    # Remove extra spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def create_fingerprint(record):
    name = normalize_for_fingerprint(
        record.get("name_or_title", "")
    )

    author = normalize_for_fingerprint(
        record.get("author", "")
    )

    source = normalize_for_fingerprint(
        record.get("source", "")
    )

    fingerprint_text = f"{source}|{name}|{author}"

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


def remove_duplicates(records):
    unique_records = []
    seen_fingerprints = set()
    duplicate_count = 0

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen_fingerprints:
            duplicate_count += 1
            continue

        seen_fingerprints.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count