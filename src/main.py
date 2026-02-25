import sys

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw

from .application import Application


def main(version):
    app = Application(version=version)
    return app.run(sys.argv)
