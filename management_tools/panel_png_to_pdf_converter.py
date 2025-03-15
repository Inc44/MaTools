from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton,
)
from module_png_to_pdf_converter import png_to_pdf_converter
from widget_draggable_list import DraggableListWidget


class PngToPdfConverterPanel(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		self.list_widget = DraggableListWidget(
			accepted_file_extensions=[".png", ".jpg"]
		)

		self.convert_button = QPushButton("Convert")
		self.convert_button.clicked.connect(self.convert_pngs_to_pdf)
		layout.addWidget(self.list_widget)
		layout.addWidget(self.convert_button)
		self.setLayout(layout)

	def convert_pngs_to_pdf(self):
		png_files_to_convert = [
			self.list_widget.item(i).text() for i in range(self.list_widget.count())
		]
		if png_files_to_convert:
			png_to_pdf_converter(png_files_to_convert)
			self.list_widget.clear()
