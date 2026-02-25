import gi
from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gio, GLib

from .window import Window


class Application(Adw.Application):

    def __init__(self, version, **kwargs):
        super().__init__(
            application_id='com.example.HelloGtkPython',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            **kwargs,
        )
        self.version = version

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self._on_about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()

    def _on_about_action(self, *args):
        about = Adw.AboutDialog(
            application_name=_('Hello GTK Python'),
            application_icon='com.example.HelloGtkPython',
            developer_name=_('Developer'),
            version=self.version,
            developers=['Developer'],
            copyright=_('\u00a9 2025 Developer'),
        )
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
