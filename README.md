
---

## 2. Final `AI_USAGE.md`

The assignment specifically requires the AI tools, their uses, representative prompts, AI-assisted areas, changes after review, incorrect/incomplete suggestions, and final verification. :chatgpt-content-reference{index="0"}

Use this:

```markdown
# AI Usage

## 1. AI Tool Used

Tool: ChatGPT

ChatGPT was used as a development assistant during the implementation of this web scraping and data-processing assignment.

The final code was reviewed, tested, and modified before submission.

## 2. What AI Was Used For

ChatGPT was used for:

- Understanding the assignment requirements.
- Designing the project structure.
- Creating initial Requests and BeautifulSoup scraper logic.
- Implementing pagination.
- Designing the common data model.
- Creating cleaning functions.
- Creating validation functions.
- Designing duplicate detection.
- Adding error handling and logging.
- Creating unit tests.
- Improving README documentation.
- Reviewing possible edge cases.

## 3. Representative Prompts

### Prompt 1 - Project Structure

"Create a beginner-friendly Python project structure for a multi-source web scraping ETL assignment using Requests and BeautifulSoup."

### Prompt 2 - Pagination

"Create a Books to Scrape scraper that automatically follows the next-page link instead of hard-coding page numbers."

### Prompt 3 - Cleaning

"Create reusable Python functions to clean whitespace, prices, ratings, and tags for scraped records."

### Prompt 4 - Validation

"Create validation logic for required fields, URLs, numeric prices, ratings, and recognized sources."

### Prompt 5 - Deduplication

"Implement duplicate detection that handles differences in capitalization, whitespace, and punctuation."

### Prompt 6 - Testing

"Create simple pytest unit tests for cleaning, validation, and duplicate detection."

## 4. AI-Assisted Parts

AI assistance was used during development of:

- `scrapers/base_scraper.py`
- `scrapers/books_scraper.py`
- `scrapers/quotes_scraper.py`
- `processing/cleaning.py`
- `processing/validation.py`
- `processing/deduplication.py`
- `main.py`
- Unit tests
- `README.md`

## 5. Important Changes After Reviewing AI Output

The generated code was reviewed instead of being used without modification.

One important improvement was made to pagination.

The initial approach constructed URLs manually using string operations such as:

```python
response.url.rsplit("/", 1)[0] + "/" + next_url