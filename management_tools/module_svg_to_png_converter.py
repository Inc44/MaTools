import os
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QImage, QPainter

from module_common_utility import get_desktop_path, get_unique_filename


def svg_to_png_converter(
	svg_path: str,
	output_dir: str = None,
	dpi: int = 300,
	image_width: int = None,
	image_height: int = None,
) -> str:
	"""
	Converts an SVG file to PNG and saves it to the given output directory.
	"""
	if output_dir is None:
		output_dir = get_desktop_path()

	output_file = os.path.join(
		output_dir, get_unique_filename("rendered", ".png", directory=output_dir)
	)

	renderer = QSvgRenderer(svg_path)
	default_size = renderer.defaultSize()

	if image_width is None and image_height is None:
		image_width = int(default_size.width() * dpi / 96)
		image_height = int(default_size.height() * dpi / 96)

	elif image_width is None:
		aspect_ratio = default_size.height() / default_size.width()
		image_width = int(image_height / aspect_ratio)
	elif image_height is None:
		aspect_ratio = default_size.width() / default_size.height()
		image_height = int(image_width / aspect_ratio)

	size = QSize(image_width, image_height)

	image = QImage(size, QImage.Format.Format_ARGB32)
	image.fill(0)

	painter = QPainter(image)
	renderer.render(painter, image.rect().toRectF())
	painter.end()

	image.save(output_file, "PNG")

	return output_file
