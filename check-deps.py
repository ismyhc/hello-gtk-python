#!/usr/bin/env python3
"""Check that all required dependencies are installed."""

import os
import shutil
import subprocess
import sys

# ── Colors ──────────────────────────────────────────────────────────────────

NO_COLOR = os.environ.get('NO_COLOR') is not None or not sys.stdout.isatty()


def _c(code, text):
    if NO_COLOR:
        return text
    return f'\033[{code}m{text}\033[0m'


def bold(text):     return _c('1', text)
def dim(text):      return _c('2', text)
def green(text):    return _c('32', text)
def yellow(text):   return _c('33', text)
def red(text):      return _c('31', text)
def cyan(text):     return _c('36', text)


# ── Checks ──────────────────────────────────────────────────────────────────

def check_command(name, args=None, min_version=None, parse_version=None):
    """Check if a command exists and optionally meets a minimum version."""
    path = shutil.which(name)
    if not path:
        return None, None

    if args is None:
        return path, None

    try:
        result = subprocess.run(
            [path] + args,
            capture_output=True, text=True, timeout=5,
        )
        output = (result.stdout + result.stderr).strip()
        if parse_version:
            version = parse_version(output)
        else:
            for token in output.split():
                if token[0].isdigit():
                    version = token.rstrip(',')
                    break
            else:
                version = output
        return path, version
    except Exception:
        return path, None


def check_gi_module(namespace, version):
    """Check if a GObject introspection module is available."""
    try:
        import gi
        gi.require_version(namespace, version)
        from gi.repository import __loader__  # noqa: F401
        __import__(f'gi.repository.{namespace}')
        return True
    except (ImportError, ValueError, Exception):
        return False


def version_tuple(v):
    try:
        return tuple(int(x) for x in v.split('.')[:3])
    except (ValueError, AttributeError):
        return (0,)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    ok = True
    warn = False

    def result(label, found, version=None, required=None, optional=False):
        nonlocal ok, warn
        if found:
            ver = dim(f' {version}') if version else ''
            if required and version and version_tuple(version) < version_tuple(required):
                print(f'  {yellow("▲")} {label}{ver}  {yellow(f"need >= {required}")}')
                if optional:
                    warn = True
                else:
                    ok = False
            else:
                print(f'  {green("✓")} {label}{ver}')
        else:
            if optional:
                print(f'  {dim("○")} {dim(label)}  {dim("not installed")}')
                warn = True
            else:
                print(f'  {red("✗")} {label}  {red("missing")}')
                ok = False

    def section(title):
        print(f'  {bold(title)}')

    print()
    print(f'  {bold("hello-gtk-python")} dependency check')
    print(f'  {"─" * 40}')
    print()

    section('Build tools')

    path, ver = check_command('meson', ['--version'], min_version='0.62.0')
    result('Meson (>= 0.62)', path, ver, '0.62')

    path, ver = check_command('ninja', ['--version'])
    result('Ninja', path, ver)

    path, ver = check_command('blueprint-compiler', ['--version'], min_version='0.14.0')
    result('Blueprint compiler (>= 0.14)', path, ver, '0.14')

    path, ver = check_command('pkg-config', ['--version'])
    result('pkg-config', path, ver)

    path, ver = check_command('glib-compile-resources', ['--version'])
    result('glib-compile-resources', path, ver)

    path, ver = check_command('glib-compile-schemas', ['--version'])
    result('glib-compile-schemas', path, ver)

    print()
    section('Python')

    path, ver = check_command('python3', ['--version'],
                              parse_version=lambda o: o.split()[-1])
    result('Python (>= 3.10)', path, ver, '3.10')

    path, ver = check_command('uv', ['--version'],
                              parse_version=lambda o: o.split()[-1])
    result('uv', path, ver)

    try:
        import gi
        result('PyGObject (python3-gi)', True, gi.__version__)
    except ImportError:
        result('PyGObject (python3-gi)', False)

    print()
    section('GObject introspection')

    result('GTK 4.0 (gir1.2-gtk-4.0)', check_gi_module('Gtk', '4.0'))
    result('Adwaita 1 (gir1.2-adw-1)', check_gi_module('Adw', '1'))

    print()
    section('Optional')

    path, ver = check_command('desktop-file-validate', ['--version'],
                              parse_version=lambda o: o.split()[-1] if o else None)
    result('desktop-file-validate', path, ver, optional=True)

    path, ver = check_command('appstreamcli', ['--version'],
                              parse_version=lambda o: o.split()[-1] if o else None)
    result('appstreamcli', path, ver, optional=True)

    path, ver = check_command('flatpak-builder', ['--version'],
                              parse_version=lambda o: o.split()[-1] if o else None)
    result('Flatpak Builder', path, ver, optional=True)

    print()
    print(f'  {"─" * 40}')
    if ok and not warn:
        print(f'  {green("✓")} {bold("All dependencies satisfied!")}')
    elif ok:
        print(f'  {green("✓")} {bold("Required dependencies satisfied.")}')
        print(f'    {dim("Some optional tools are not installed.")}')
    else:
        print(f'  {red("✗")} {bold("Some required dependencies are missing.")}')
        print()
        print(f'  {cyan("On Ubuntu/Debian, install with:")}')
        print(f'  {dim("$")} sudo apt install python3-gi python3-gi-cairo gir1.2-adw-1 \\')
        print(f'      meson ninja-build blueprint-compiler pkg-config \\')
        print(f'      libglib2.0-dev-bin')

    print()
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
