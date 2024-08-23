application_id = 'com.lapas.Fbe'

scalable_dir = 'hicolor' / 'scalable' / 'apps'
scalable_icons = [
	scalable_dir / 'fbe.svg',
	scalable_dir / 'add.png',
	scalable_dir / 'connect.png',
	scalable_dir / 'delete.png',
	scalable_dir / 'move.png',
	scalable_dir / 'edit.png',
	scalable_dir / 'save.png',
	scalable_dir / 'save_as.png',
	scalable_dir / 'new_fb.png',
	scalable_dir / ('@0@.svg').format(application_id),
	scalable_dir / 'plus-symbolic.svg',
	scalable_dir / 'inspect_fb.png',
	scalable_dir / 'new_file.png',
	scalable_dir / 'directory.png',
	scalable_dir / 'left_arrow.png',
	scalable_dir / 'right_arrow.png',
	scalable_dir / 'big_right_arrow.png',
	scalable_dir / 'big_left_arrow.png'
]
install_data(
  scalable_icons,
  install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)
