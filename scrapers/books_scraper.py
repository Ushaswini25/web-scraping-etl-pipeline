from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    START_URL = "https://books.toscrape.com/"

    def scrape(self):
        books = []
        current_url = self.START_URL

        while current_url:
            response = self.get_page(current_url)

            if response is None:
                break

            soup = BeautifulSoup(response.text, "lxml")

            book_items = soup.select("article.product_pod")

            for book in book_items:
                title_element = book.select_one("h3 a")
                price_element = book.select_one("p.price_color")
                rating_element = book.select_one("p.star-rating")

                title = (
                    title_element.get("title", "")
                    if title_element
                    else ""
                )

                price = (
                    price_element.get_text(strip=True)
                    if price_element
                    else ""
                )

                rating = ""

                if rating_element:
                    rating_classes = rating_element.get("class", [])

                    for class_name in rating_classes:
                        if class_name != "star-rating":
                            rating = class_name
                            break

                book_url = ""

                if title_element:
                    book_url = title_element.get("href", "")

                    book_url = response.url.rsplit("/", 1)[0] + "/" + book_url

                books.append({
                    "source": "books_to_scrape",
                    "source_url": book_url,
                    "name_or_title": title,
                    "category": "",
                    "price": price,
                    "rating": rating,
                    "author": "",
                    "tags": "",
                    "description": "",
                })

            next_button = soup.select_one("li.next a")

            if next_button:
                next_url = next_button.get("href")

                current_url = response.url.rsplit("/", 1)[0] + "/" + next_url
            else:
                current_url = None

        return books