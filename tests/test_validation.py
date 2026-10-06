from processing.validation import (
    is_valid_url,
    validate_record,
    is_valid_record,
)


def test_valid_url():
    assert is_valid_url(
        "https://example.com/page"
    )


def test_invalid_url():
    assert not is_valid_url(
        "not-a-valid-url"
    )


def test_valid_record():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://example.com/book",
        "name_or_title": "Example Book",
        "price": "20.50",
        "rating": "4",
    }

    assert is_valid_record(record)


def test_invalid_source():
    record = {
        "source": "unknown_source",
        "source_url": "https://example.com",
        "name_or_title": "Example",
        "price": "20",
        "rating": "4",
    }

    errors = validate_record(record)

    assert "Invalid source" in errors


def test_invalid_price():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://example.com",
        "name_or_title": "Example",
        "price": "abc",
        "rating": "4",
    }

    errors = validate_record(record)

    assert "Invalid price" in errors


def test_invalid_rating():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://example.com",
        "name_or_title": "Example",
        "price": "20",
        "rating": "10",
    }

    errors = validate_record(record)

    assert "Invalid rating" in errors