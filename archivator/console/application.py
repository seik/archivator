#!/usr/bin/env python

from archivator.console.archive import ArchiveCommand
from cleo import Application

application = Application()
application.add(ArchiveCommand().default())

if __name__ == "__main__":
    application.run()


def cli():
    application.run()
