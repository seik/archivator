from cleo import Command

from url_normalize import url_normalize
from archivator.console.exceptions import URLDoesNotExist
from archivator.archivator import Archivator
from archivator.console.validators import validate_url
from archivator.archiveorg import InternetArchive


class ArchiveCommand(Command):
    """
    Archives a page

    archive
        {url : Page url}
        {--u|unique : If set, archive only that link}
    """

    def handle(self) -> None:
        url = url_normalize(self.argument("url"))

        try:
            validated_url = validate_url(url)
        except URLDoesNotExist:
            self.line("<error>This page does not seem to exist</error>")

        try:
            self.page(validated_url) if not self.option("unique") else self.unique(
                validated_url
            )
        except InternetArchive.TooManyRequestsError:
            self.line("")
            self.error("Limited by archive.org, please try again later")

    def unique(self, url):
        self.write("Archiving...")
        archived_url, cached = Archivator.archive_url(url)
        if not cached:
            self.line(f"Archived in {archived_url}")
        else:
            self.line("Page was archived recently, saving skiped by archive.org.")

    def page(self, url):
        archivator = Archivator(url, cleo_command=self)
        archivator.run()

    def write(self, new_line=True, overwrite=False):
        self.write
