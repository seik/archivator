from typing import Tuple
from urllib.parse import urljoin

import requests


class InternetArchive:
    def __init__(self, api_url=None):
        self.api_url = api_url or "https://web.archive.org"
        self.user_agent = "archivator.py"
        self.save_url = urljoin(self.api_url, "/save/")

    class BlockedError(Exception):
        """
        Returned when archive.org has been banned from the site
        """

    class ArchiveError(Exception):
        """
        General exception for general errors
        """

    def archive_page(self, url: str) -> Tuple[str, bool]:
        archive_url = f"{self.save_url}{url}"
        response = requests.get(archive_url, headers={"User-Agent": self.user_agent})

        has_error_header = "X-Archive-Wayback-Runtime-Error" in response.headers
        if has_error_header:
            error_header = response.headers["X-Archive-Wayback-Runtime-Error"]
            if error_header == "RobotAccessControlException: Blocked By Robots":
                raise BlockedError("archive.org returned blocked by robots.txt error")
            else:
                raise self.ArchiveError(error_header)

        if response.status_code in [403, 502]:
            raise self.ArchiveError(response.headers)

        try:
            archive_id = response.headers["Content-Location"]
        except KeyError:
            # If it can't find that key raise the error
            raise self.ArchiveError(
                dict(status_code=response.status_code, headers=response.headers)
            )

        archive_url = urljoin(self.api_url, archive_id)

        cached = (
            "X-Page-Cache" in response.headers
            and response.headers["X-Page-Cache"] == "HIT"
        )
        return archive_url, cached
