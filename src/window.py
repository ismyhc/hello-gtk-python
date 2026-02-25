import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path='/com/example/HelloGtkPython/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'HelloGtkPythonWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
