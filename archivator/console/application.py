#!/usr/bin/env python

from archivator.console.archive import ArchiveCommand
from cleo import Application

application = Application()
application.add(ArchiveCommand())

if __name__ == "__main__":
    application.run()
