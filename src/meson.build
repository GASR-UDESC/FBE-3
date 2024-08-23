pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'fbe'
gnome = import('gnome')

gnome.compile_resources('fbe',
  'fbe.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'fbe.in',
  output: 'fbe',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

fbe_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'fb_editor.py',
  'ecc_editor.py',
  'ecc_renderer.py',
  'fb_renderer.py',
  'base.py',
  'function_block.py',
  'xmlParser.py',
  'system_editor.py',
  'project_editor.py',
  'system_config_editor.py',
  'system_renderer.py',
  'export.py'
]

install_data(fbe_sources, install_dir: moduledir)
