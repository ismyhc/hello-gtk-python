pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'hello_gtk_python'

blueprints = custom_target('blueprints',
  input: files(
    'window.blp',
  ),
  output: '.',
  command: [
    find_program('blueprint-compiler'),
    'batch-compile',
    '@OUTPUT@',
    '@CURRENT_SOURCE_DIR@',
    '@INPUT@',
  ],
)

gnome.compile_resources('hello-gtk-python',
  'hello-gtk-python.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'hello-gtk-python.in',
  output: 'hello-gtk-python',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

# Dev launcher for local `ninja run`
dev_conf = configuration_data()
dev_conf.set('PYTHON', py_installation.full_path())
dev_conf.set('VERSION', meson.project_version())
dev_conf.set('localedir', meson.project_source_root() / 'po')
dev_conf.set('pkgdatadir', meson.project_build_root() / 'src')

configure_file(
  input: 'hello-gtk-python.in',
  output: 'dev-run',
  configuration: dev_conf,
)

hello_gtk_python_sources = [
  '__init__.py',
  'main.py',
  'application.py',
  'window.py',
]

install_data(hello_gtk_python_sources, install_dir: moduledir)
