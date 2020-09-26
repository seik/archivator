import html
from time import sleep
from typing import Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from archivator.archiveorg import InternetArchive
import sys


class Archivator:
    def __init__(self, start_url, writer=sys.stdout):
        parsed_url = urlparse(start_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.start_url = start_url
        self.scraped_urls = set()
        self.urls_to_scrape = set([self.start_url])

        self._writer = writer
        self._last_message_len = 0
        self._last_write_overwrite = False

    @staticmethod
    def archive_url(url: str) -> Tuple[str, bool]:
        """
        Static method used to archive a single link
        """
        internet_archive = InternetArchive()
        return internet_archive.archive_page(url)

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
        self.write(f"")
        for url in self.scraped_urls:
            self.overwrite(f"🗄️  {url}")
            archive_url, cached = internet_archive.archive_page(url)

    def run(self):
        self.write(f"")

        while self.urls_to_scrape:
            current_url = self.urls_to_scrape.pop()

            urls = self.collect_page_urls(current_url)
            self.scraped_urls.add(current_url)
            for url in urls:
                if url not in self.scraped_urls and url not in self.urls_to_scrape:
                    self.urls_to_scrape.add(url)

            self.overwrite(f"🕵️  {current_url}")

        self.line("")
        self.line(f"📣 Collected {len(self.scraped_urls)} URLs")
        self.line(f"📦 Archiving")

        self.archive_urls()

        self.line("")
        self.line(f"✅ Everything has been archived")

    def line(self, text: str) -> None:
        if self._writer:
            self._writer.write(text)
            self._writer.flush()
            self._last_message_len = len(text)
            self._last_write_overwrite = False

    def write(self, text: str) -> None:
        if self._writer:
            self._writer.write(text)
            self._writer.write("\n")
            self._writer.flush()

            self._last_message_len = len(text)
            self._last_write_overwrite = False

    def overwrite(self, text: str) -> None:
        if self._writer:
            self._writer.write
            self._writer.write(
                " ".join(["\b" for _ in range(self._last_write_overwrite + 20)])
            )
            self._writer.flush()
            self._writer.write(
                " ".join([" " for _ in range(self._last_write_overwrite + 20)])
            )
            self._writer.write(f"\r{text}")
            self._writer.flush()

            self._last_message_len = len(text)
            self._last_write_overwrite = True
