import requests
from requests.exceptions import ConnectionError

from archivator.console.exceptions import URLDoesNotExist


def validate_url(url: str) -> str:
    try:
        requests.get(url)
    except ConnectionError:
        raise URLDoesNotExist
    else:
        return url
