from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

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

    def collect_page_urls(self, url: str):
        response = requests.get(url)
        hrefs = list(
            filter(
                lambda doctype: doctype.has_attr("href"),
                BeautifulSoup(
                    response.text, features="html.parser", parse_only=SoupStrainer("a")
                ),
            ),
        )
        urls = [f"{element['href']}" for element in hrefs]
        relative_urls = list(filter(self.validate_url, urls))
        return [f"{self.base_url}{url}" for url in relative_urls]

    def validate_url(self, url: str):
        return self.check_is_site_url(url) and not self.check_is_base(url)

    def archive_urls(self):
        internet_archive = InternetArchive()
        for url in self.scraped_urls:
            sleep(0.5)
            internet_archive.archive_page(url)

    def run(self):
        while self.urls_to_scrape:
            current_url = self.urls_to_scrape.pop()
            urls = self.collect_page_urls(current_url)
            # TODO: Add logging debug for information
            self.scraped_urls.add(current_url)
            for url in urls:
                if url not in self.scraped_urls and url not in self.urls_to_scrape:
                    self.urls_to_scrape.add(url)
        self.archive_urls()

scraper = Scraper("https://www.es.python.org/index.html")
scraper.run()
