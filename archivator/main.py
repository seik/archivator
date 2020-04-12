from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from loguru import logger
import html
from archivator.archiveorg import InternetArchive


class Scraper:
    def __init__(self, start_url):
        parsed_url = urlparse(start_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.start_url = start_url
        self.scraped_urls = set()
        self.urls_to_scrape = set([start_url])

    def check_is_site_url(self, url: str) -> bool:
        return bool(url.startswith("/") or self.base_url in url)

    def check_is_base(self, url: str) -> bool:
        # FIXME: This method doesn't cover all cases
        return url in ["/", f"{self.base_url}/", f"{self.base_url}"]

    def check_not_visited(self, url: str) -> bool:
        pass

    def clean_url(self, url: str) -> str:
        cleaned_url = f"{self.base_url}{url}" if url.startswith("/") else url
        return html.unescape(cleaned_url)

    def collect_page_urls(self, url: str):
        response = requests.get(url)
        if "text/html" in response.headers["Content-Type"]:
            hrefs = list(
                filter(
                    lambda doctype: doctype.has_attr("href"),
                    BeautifulSoup(
                        response.text,
                        features="html.parser",
                        parse_only=SoupStrainer("a"),
                    ),
                ),
            )
            urls = [f"{element['href']}" for element in hrefs]
            relative_urls = list(filter(self.validate_url, urls))
            page_urls = [self.clean_url(url) for url in relative_urls]
        else:
            page_urls = []
        return page_urls

    def validate_url(self, url: str):
        return self.check_is_site_url(url) and not self.check_is_base(url)

    def archive_urls(self):
        internet_archive = InternetArchive()
        for url in self.scraped_urls:
            internet_archive.archive_page(url)
            logger.info(f"Archived: {url}")

    def run(self):
        while self.urls_to_scrape:
            current_url = self.urls_to_scrape.pop()
            urls = self.collect_page_urls(current_url)
            self.scraped_urls.add(current_url)
            logger.info(f"Scrapping {current_url}")
            for url in urls:
                if url not in self.scraped_urls and url not in self.urls_to_scrape:
                    self.urls_to_scrape.add(url)
                    logger.info(f"Found {url}")

        logger.info(f"Collected {len(self.scraped_urls)} URLs")
        logger.info(f"Start archiving")

        self.archive_urls()


scraper = Scraper("https://ivmg.me/")
scraper.run()
