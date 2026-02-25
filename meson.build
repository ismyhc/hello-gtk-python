project('hello-gtk-python',
  version: '0.1.0',
  meson_version: '>= 0.62.0',
)

i18n = import('i18n')
gnome = import('gnome')

python = import('python')
fs = import('fs')

# Prefer the uv venv so meson and runtime share the same environment.
# Falls back to system Python (e.g. inside flatpak-builder).
venv_python = meson.project_source_root() / '.venv' / 'bin' / 'python3'
if fs.exists(venv_python)
  py_installation = python.find_installation(venv_python)
else
  py_installation = python.find_installation('python3')
endif

dependency('gtk4', version: '>= 4.0')
dependency('libadwaita-1', version: '>= 1.0')

subdir('data')
subdir('po')
subdir('src')

dev_cmd = 'ln -sfn "@0@/src" "@1@/src/hello_gtk_python" && '.format(
  meson.project_source_root(), meson.project_build_root(),
) + 'glib-compile-schemas "@0@/data" 2>/dev/null; '.format(
  meson.project_source_root(),
) + 'GSETTINGS_SCHEMA_DIR="@0@/data" exec "@1@" "@2@/src/dev-run"'.format(
  meson.project_source_root(),
  py_installation.full_path(),
  meson.project_build_root(),
)

run_target('run',
  command: [find_program('sh'), '-c', dev_cmd],
)

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
