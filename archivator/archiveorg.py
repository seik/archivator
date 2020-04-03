from urllib.parse import urljoin
import requests


class InternetArchive:
    def __init__(self, api_url=None):
        self.api_url = api_url or "https://web.archive.org"
        self.user_agent = "archivator.py"
        self.save_url = urljoin(self.api_url, "/save/")

    def archive_page(self, url: str):
        archive_url = f"{self.save_url}{url}"
        requests.get(archive_url, headers={"User-Agent": self.user_agent})
