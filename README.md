# Hello GTK Python

A GTK4/Adwaita application template built with Python and Blueprint.

## Project Structure

```
hello-gtk-python/
├── meson.build                              # Root build definition
├── com.example.HelloGtkPython.json          # Flatpak manifest
├── pyproject.toml                           # Python project metadata
├── rename.py                                # Project renamer script
├── data/
│   ├── com.example.HelloGtkPython.desktop.in # Desktop entry
│   ├── com.example.HelloGtkPython.metainfo.xml.in # AppStream metadata
│   ├── com.example.HelloGtkPython.gschema.xml     # GSettings schema
│   └── icons/                               # App icons (scalable + symbolic)
├── po/                                      # i18n translations
└── src/
    ├── meson.build                          # Blueprint compile + GResource + Python install
    ├── hello-gtk-python.in                  # Meson-configured launcher script
    ├── main.py                              # Entry point
    ├── application.py                       # Adw.Application subclass
    ├── window.py                            # Adw.ApplicationWindow subclass
    └── window.blp                           # Blueprint UI definition
```

## Dependencies

- Python 3.10+
- GTK 4
- libadwaita 1
- Meson >= 0.62
- blueprint-compiler >= 0.14
- PyGObject
- uv

Install uv (Python package manager):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check if everything is installed:

```bash
python3 check-deps.py
```

On Ubuntu/Debian:

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-adw-1 meson ninja-build blueprint-compiler
```

On Fedora:

```bash
sudo dnf install python3-gobject python3-gobject-devel gtk4-devel libadwaita-devel meson ninja-build blueprint-compiler
```

## Building

### Local Development

```bash
# Initial setup (one time)
uv venv --system-site-packages
uv sync
meson setup build

# Build and run
meson compile -C build && ninja -C build run
```

The `--system-site-packages` flag gives the venv access to PyGObject (system package).
Meson auto-detects the `.venv` Python, so the launcher and any `uv add` dependencies
share the same environment. Changes to `.blp` files are recompiled on each build.

To add Python dependencies:

```bash
uv add requests  # or any pip package
```

### Flatpak

Requires the GNOME 48 SDK:

```bash
# Install runtime and SDK (one time)
flatpak remote-add --if-not-exists --user flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.gnome.Sdk//48 org.gnome.Platform//48

# Build and install
flatpak-builder --user --install --force-clean build-flatpak com.example.HelloGtkPython.json

# Run
flatpak run com.example.HelloGtkPython
```

## Make It Your Own

Run the rename script to replace all template names with your own:

```bash
uv run rename.py
```

It will prompt for:

- **Project name** (kebab-case, e.g. `my-cool-app`)
- **Application ID** (e.g. `com.mycompany.MyCoolApp`)
- **Display name** (e.g. `My Cool App`)

This renames all files and replaces every instance of `hello-gtk-python`, `HelloGtkPython`, `com.example.HelloGtkPython`, etc. throughout the project. Any existing build directories are automatically cleaned up.

After renaming, re-run the initial setup:

```bash
uv venv --system-site-packages
uv sync
meson setup build
meson compile -C build && ninja -C build run
```

**Note:** Commands elsewhere in this README that reference `hello-gtk-python` or
`com.example.HelloGtkPython` will need to use your new project name and application ID instead
(e.g. `ninja -C build my-cool-app-pot`, `flatpak run com.mycompany.MyCoolApp`).

## Translations (i18n)

Wrap user-visible strings with `_()` to make them translatable:

- **Blueprint**: `label: _("Hello, World!");`
- **Python**: `_('Hello, World!')` (add `from gettext import gettext as _` at the top)

Any new source files with `_()` strings must be listed in `po/POTFILES`.

After adding or changing translatable strings:

```bash
# Regenerate the .pot template and merge into .po files
ninja -C build hello-gtk-python-pot
ninja -C build hello-gtk-python-update-po
```

To add a new language (e.g. French):

1. Create `po/fr.po` from the `.pot` template: `msginit -i po/hello-gtk-python.pot -o po/fr.po -l fr`
2. Add `fr` to `po/LINGUAS`
3. Translate the `msgstr` entries in `po/fr.po`

The build compiles `.po` files into binary `.mo` files automatically.

## Documentation

- [GTK 4 — Python API Reference](https://lazka.github.io/pgi-docs/Gtk-4.0/)
- [Libadwaita — Python API Reference](https://lazka.github.io/pgi-docs/Adw-1/)
- [Blueprint — UI Language](https://gnome.pages.gitlab.gnome.org/blueprint-compiler)
- [PyGObject](https://pygobject.gnome.org/)
- [Meson Build System](https://mesonbuild.com/)
- [Flatpak Builder](https://docs.flatpak.org/en/latest/flatpak-builder.html)
- [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/)

## License

MIT
