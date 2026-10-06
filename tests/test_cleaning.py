from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags,
    clean_record,
)


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == "51.77"


def test_clean_rating():
    assert clean_rating("Three") == "3"


def test_clean_tags():
    assert clean_tags(" fiction,  classic ") == "fiction, classic"


def test_clean_record():
    record = {
        "source": "  books_to_scrape  ",
        "source_url": " https://example.com ",
        "name_or_title": "  A   Great   Book ",
        "category": "",
        "price": "£25.50",
        "rating": "Five",
        "author": "",
        "tags": " fiction, classic ",
        "description": "  Good book  ",
    }

    cleaned = clean_record(record)

    assert cleaned["source"] == "books_to_scrape"
    assert cleaned["name_or_title"] == "A Great Book"
    assert cleaned["price"] == "25.50"
    assert cleaned["rating"] == "5"
    assert cleaned["tags"] == "fiction, classic"
    assert cleaned["description"] == "Good book"