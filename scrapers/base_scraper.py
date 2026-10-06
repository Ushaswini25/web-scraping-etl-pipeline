import logging #logging records
import time # allow us to pause between requests

import requests # downloads the webpage

# below 2 are automatically retry temporary failures
from requests.adapters import HTTPAdapter 
from urllib3.util import Retry


logger = logging.getLogger(__name__)


class BaseScraper: #shared scraper class
    def __init__(self):
        self.session = self.create_session()
        self.timeout = 10
        self.delay = 0.5

    def create_session(self):
        session = requests.Session()

        session.headers.update({
            "User-Agent": "ScrapingAssignment/1.0 (learning project)"
        })

        retries = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retries)

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def get_page(self, url):
        logger.info("Requesting page: %s", url)

        try:
            response = self.session.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()
            response.encoding = "utf-8"

            logger.info(
                "Successfully fetched %s - Status: %s",
                url,
                response.status_code
            )

            time.sleep(self.delay)

            return response

        except requests.RequestException as exc:
            logger.error(
                "Failed to fetch %s: %s",
                url,
                exc
            )

            return None