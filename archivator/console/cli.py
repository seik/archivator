from time import sleep

import click
from click import secho as click_echo
from url_normalize import url_normalize

from archivator.archivator import Archivator
from archivator.cli.exceptions import URLDoesNotExist
from archivator.cli.validators import validate_url


import subprocess


@click.command()
@click.argument("url", nargs=1)
@click.option("-u", "--unique", help="Archive an unique page.", is_flag=True)
def archive(url, unique):
    url = url_normalize(url)
    try:
        validated_url = validate_url(url)
    except URLDoesNotExist:
        echo("Error: This page does not seem to exist", fg="red", err=True)
    else:
        archive_page(validated_url) if not unique else archive_unique(validated_url)


def archive_unique(url):
    echo("Archiving...")
    archived_url, cached = Archivator.archive_url(url)
    if not cached:
        echo(f"Archived in {archived_url}")
    else:
        echo("Page was archived recently, saving skiped by archive.org.")


def archive_page(url):
    archivator = Archivator(url, stdout=echo)
    archivator.run()


def echo(
    message=None,
    file=None,
    nl=True,
    err=False,
    color=None,
    carriage_return=False,
    clean=True,
    **kwargs,
):
    """
    Patched click echo function.
    """
    message = message or ""

    if clean:
        rows, columns = subprocess.check_output(["stty", "size"]).split()
        line_size = " ".join([" " for i in range(int(columns) - 40)])
        # print(int(columns))
        # print(len(line_size))
        click_echo("\033[K", file, False, err, color, **kwargs)

    if carriage_return and nl:
        click_echo(message + "\r\n", file, False, err, color, **kwargs)
    elif carriage_return and not nl:
        click_echo(message + "\r", file, False, err, color, **kwargs)
    else:
        click_echo(message, file, nl, err, color, **kwargs)


if __name__ == "__main__":
    archive()
