from processing.deduplication import (
    create_fingerprint,
    remove_duplicates,
)


def test_same_records_have_same_fingerprint():
    record1 = {
        "source": "books_to_scrape",
        "name_or_title": "Example Book",
        "author": "",
    }

    record2 = {
        "source": "books_to_scrape",
        "name_or_title": " example   book ",
        "author": "",
    }

    assert create_fingerprint(record1) == (
        create_fingerprint(record2)
    )


def test_remove_duplicates():
    records = [
        {
            "source": "books_to_scrape",
            "name_or_title": "Example Book",
            "author": "",
        },
        {
            "source": "books_to_scrape",
            "name_or_title": "Example Book",
            "author": "",
        },
        {
            "source": "quotes_to_scrape",
            "name_or_title": "Example Quote",
            "author": "Author",
        },
    ]

    unique_records, duplicate_count = (
        remove_duplicates(records)
    )

    assert len(unique_records) == 2
    assert duplicate_count == 1