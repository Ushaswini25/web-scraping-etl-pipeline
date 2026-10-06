import re


def clean_text(value):
    if value is None:
        return ""

    value = str(value)

    # Remove extra whitespace
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def clean_price(value):
    value = clean_text(value)

    if not value:
        return ""

    # Keep only numbers and decimal point
    cleaned = re.sub(r"[^\d.]", "", value)

    return cleaned


def clean_rating(value):
    value = clean_text(value)

    if not value:
        return ""

    rating_map = {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5",
    }

    return rating_map.get(value, value)


def clean_tags(value):
    value = clean_text(value)

    if not value:
        return ""

    tags = [tag.strip() for tag in value.split(",")]

    return ", ".join(tags)


def clean_record(record):
    cleaned_record = record.copy()

    cleaned_record["source"] = clean_text(
        cleaned_record.get("source", "")
    )

    cleaned_record["source_url"] = clean_text(
        cleaned_record.get("source_url", "")
    )

    cleaned_record["name_or_title"] = clean_text(
        cleaned_record.get("name_or_title", "")
    )

    cleaned_record["category"] = clean_text(
        cleaned_record.get("category", "")
    )

    cleaned_record["price"] = clean_price(
        cleaned_record.get("price", "")
    )

    cleaned_record["rating"] = clean_rating(
        cleaned_record.get("rating", "")
    )

    cleaned_record["author"] = clean_text(
        cleaned_record.get("author", "")
    )

    cleaned_record["tags"] = clean_tags(
        cleaned_record.get("tags", "")
    )

    cleaned_record["description"] = clean_text(
        cleaned_record.get("description", "")
    )

    return cleaned_record