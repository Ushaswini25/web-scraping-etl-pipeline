import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class QuotesScraper(BaseScraper):
    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        quotes = []
        current_url = self.START_URL

        while current_url:
            response = self.get_page(current_url)

            if response is None:
                logger.error("Skipping failed page: %s", current_url)
                break

            soup = BeautifulSoup(response.text, "lxml")

            quote_items = soup.select("div.quote")

            for quote in quote_items:
                text_element = quote.select_one("span.text")
                author_element = quote.select_one("small.author")
                tag_elements = quote.select("a.tag")

                quote_text = (
                    text_element.get_text(strip=True)
                    if text_element
                    else ""
                )

                author = (
                    author_element.get_text(strip=True)
                    if author_element
                    else ""
                )

                tags = ", ".join(
                    tag.get_text(strip=True)
                    for tag in tag_elements
                )

                quotes.append({
                    "source": "quotes_to_scrape",
                    "source_url": response.url,
                    "name_or_title": quote_text,
                    "category": "",
                    "price": "",
                    "rating": "",
                    "author": author,
                    "tags": tags,
                    "description": "",
                })

            next_button = soup.select_one("li.next a")

            if next_button:
                next_url = next_button.get("href", "")
                current_url = urljoin(response.url, next_url)
            else:
                current_url = None

        return quotes