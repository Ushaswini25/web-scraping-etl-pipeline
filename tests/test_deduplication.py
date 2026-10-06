from processing.deduplication import (
    normalize_for_fingerprint,
    create_fingerprint,
    remove_duplicates,
)


def test_normalize_for_fingerprint():
    value = "  Hello,   WORLD!  "

    assert normalize_for_fingerprint(value) == "hello world"


def test_same_fingerprint_for_similar_values():
    record1 = {
        "source": "quotes_to_scrape",
        "name_or_title": "The World Is Beautiful!",
        "author": "Albert Einstein",
    }

    record2 = {
        "source": "quotes_to_scrape",
        "name_or_title": "the world is beautiful",
        "author": "albert einstein",
    }

    assert create_fingerprint(record1) == create_fingerprint(record2)


def test_remove_duplicates():
    records = [
        {
            "source": "quotes_to_scrape",
            "name_or_title": "Hello World!",
            "author": "Author One",
        },
        {
            "source": "quotes_to_scrape",
            "name_or_title": "hello world",
            "author": "author one",
        },
        {
            "source": "quotes_to_scrape",
            "name_or_title": "Another Quote",
            "author": "Author Two",
        },
    ]

    unique_records, duplicate_count = remove_duplicates(records)

    assert len(unique_records) == 2
    assert duplicate_count == 1