import requests
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from urllib.parse import urlparse


class Scrapper:
    def __init__(self, start_url):
        parsed_url = urlparse(start_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.start_url = start_url
        self.urls_to_scrape = [start_url]

    def check_is_site_url(self, url: str) -> bool:
        return bool(url.startswith("/") or self.base_url in url)

    def check_is_base(self, url: str) -> bool:
        parsed_url = urlparse(f"{self.base_url}{url}")
        return (
            f"{self.base_url}/"
            == f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
        )

    def check_not_visited(self, url: str) -> bool:
        pass

    def collect_page_urls(self, url:str):
        response = requests.get(url)
        hrefs = list(filter(
            lambda doctype: doctype.has_attr("href"),
            BeautifulSoup(
                response.text, features="html.parser", parse_only=SoupStrainer("a")
            )),
        )
        urls = [element["href"] for element in hrefs]
        return list(filter(self.validate_url, urls))

    def validate_url(self, url: str):
        return self.check_is_site_url(url) and not self.check_is_base(url)

    def run(self):
        while self.urls_to_scrape:
            current_url = self.urls_to_scrape.pop()
            self.urls_to_scrape.append(self.scrapper.collect_current_page_urls(current_url))


scrapper = Scrapper("https://www.es.python.org/index.html")
scrapper.run()
