from processing.validation import (
    validate_record,
    is_valid_record,
)


def test_valid_record():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "A Light in the Attic",
        "price": "51.77",
        "rating": "3",
    }

    assert is_valid_record(record) is True
    assert validate_record(record) == []


def test_missing_title():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "",
        "price": "51.77",
        "rating": "3",
    }

    assert is_valid_record(record) is False


def test_invalid_url():
    record = {
        "source": "books_to_scrape",
        "source_url": "invalid-url",
        "name_or_title": "Test Book",
        "price": "51.77",
        "rating": "3",
    }

    errors = validate_record(record)

    assert "Invalid source_url" in errors


def test_invalid_price():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": "abc",
        "rating": "3",
    }

    errors = validate_record(record)

    assert "Invalid price" in errors


def test_invalid_rating():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": "10.50",
        "rating": "10",
    }

    errors = validate_record(record)

    assert "Invalid rating" in errors