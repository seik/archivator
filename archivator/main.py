import requests
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from urllib.parse import urlparse


class Scraper:
    def __init__(self, start_url):
        parsed_url = urlparse(start_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.start_url = start_url
        self.urls_to_scrape = [start_url]

    def check_is_site_url(self, url: str) -> bool:
        return bool(url.startswith("/") or self.base_url in url)

    def check_is_base(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}" in [
            f"{self.base_url}/",
            f"{self.base_url}",
        ]

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
        urls = [f"{self.base_url}{element['href']}" for element in hrefs]
        return list(filter(self.validate_url, urls))

    def validate_url(self, url: str):
        return self.check_is_site_url(url) and not self.check_is_base(url)

    def run(self):

        # while self.urls_to_scrape:
        current_url = self.urls_to_scrape.pop()
        self.urls_to_scrape.extend(self.collect_page_urls(current_url))
        for url in self.urls_to_scrape:
            print(url)


scraper = Scraper("https://www.es.python.org/index.html")
scraper.run()
