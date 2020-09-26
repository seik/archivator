import typer
from archivator.archivator import Archivator
from archivator.archiveorg import InternetArchive
from archivator.console.exceptions import URLDoesNotExist
from archivator.console.validators import validate_url
from url_normalize import url_normalize

app = typer.Typer()


@app.command()
def archive(
    url: str, unique: bool = typer.Option(False, help="If set, archive only that link"),
):
    url = url_normalize(url)

    try:
        validated_url = validate_url(url)
    except URLDoesNotExist:
        typer.echo("This page does not seem to exist", err=True)
        raise typer.Abort()

    try:
        page(validated_url) if not unique else single_page(validated_url)
    except InternetArchive.TooManyRequestsError:
        typer.echo("")
        typer.echo("Limited by archive.org, please try again later", err=True)


def single_page(url: str):
    typer.echo("Archiving...")
    archived_url, cached = Archivator.archive_url(url)
    if not cached:
        typer.echo(f"Archived in {archived_url}")
    else:
        typer.echo("Page was archived recently, saving skiped by archive.org.")


def page(url):
    archivator = Archivator(url)
    archivator.run()


if __name__ == "__main__":
    typer.run(archive)


def cli():
    typer.run(archive)
