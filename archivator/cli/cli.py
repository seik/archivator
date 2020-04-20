import click
from url_normalize import url_normalize

from archivator.archivator import Archivator
from archivator.cli.exceptions import URLDoesNotExist
from archivator.cli.validators import validate_url


@click.command()
@click.argument("url", nargs=1)
@click.option("-s", "--single", help="Scrape a single page.", is_flag=True)
def archive(url, single):
    url = url_normalize(url)
    try:
        validated_url = validate_url(url)
    except URLDoesNotExist:
        click.echo("ERROR: This page does not seem to exist")
    else:
        archive_single(validated_url) if single else archive_page(validated_url)


def archive_single(url):
    click.echo("Archiving...")
    archived_url, cached = Archivator.archive_url(url)
    if not cached:
        click.echo(f"Archived in {archived_url}")
    else:
        click.echo("Page was archived recently, saving skiped by internet archive.")


def archive_page(url):
    archivator = Archivator(url)
    archivator.run()


if __name__ == "__main__":
    archive()