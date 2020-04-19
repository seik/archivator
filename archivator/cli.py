import click
from archivator.archivator import Archivator


def single_link(url):
    click.echo("Archiving...")
    archived_url, cached = Archivator.archive_url(url)
    if not cached:
        click.echo(f"Archived in {archived_url}")
    else:
        click.echo("Page was archived recently, skiped by internet archive.")


def site(url):
    archivator = Archivator(url)
    archivator.run()


@click.command()
@click.argument("url", nargs=1)
@click.option("-s", "--single", help="Scrape a single page.", is_flag=True)
def archive(url, single):
    if single:
        single_link(url)
    else:
        site(url)


if __name__ == "__main__":
    archive()
