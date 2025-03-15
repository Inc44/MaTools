from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QLabel,
	QPushButton,
	QLineEdit,
	QFileDialog,
)
from module_svg_to_png_converter import svg_to_png_converter
from widget_draggable_list import DraggableListWidget


class SvgToPngConverterPanel(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout(self)

		self.image_width_label = QLabel("Image Width:", self)
		self.image_width_edit = QLineEdit(self)
		layout.addWidget(self.image_width_label)
		layout.addWidget(self.image_width_edit)

		self.image_height_label = QLabel("Image Height:", self)
		self.image_height_edit = QLineEdit(self)
		layout.addWidget(self.image_height_label)
		layout.addWidget(self.image_height_edit)

		self.dpi_label = QLabel("DPI:", self)
		self.dpi_edit = QLineEdit(self)
		layout.addWidget(self.dpi_label)
		layout.addWidget(self.dpi_edit)

		self.output_path_label = QLabel("Output Path:", self)
		self.output_path_edit = QLineEdit(self)
		self.browse_button = QPushButton("Browse...", self)
		self.browse_button.clicked.connect(self.browse_output_path)
		layout.addWidget(self.output_path_label)
		layout.addWidget(self.output_path_edit)
		layout.addWidget(self.browse_button)

		self.list_widget = DraggableListWidget(accepted_file_extensions=[".svg"])
		layout.addWidget(self.list_widget)

		self.convert_button = QPushButton("Convert", self)
		self.convert_button.clicked.connect(self.perform_conversion)
		layout.addWidget(self.convert_button)
		self.setLayout(layout)

	def browse_output_path(self):
		directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
		if directory:
			self.output_path_edit.setText(directory)

	def perform_conversion(self):
		output_path = (
			self.output_path_edit.text().strip()
			if self.output_path_edit.text().strip()
			else None
		)
		dpi = int(self.dpi_edit.text()) if self.dpi_edit.text().strip() else 300
		image_width = (
			int(self.image_width_edit.text())
			if self.image_width_edit.text().strip()
			else None
		)
		image_height = (
			int(self.image_height_edit.text())
			if self.image_height_edit.text().strip()
			else None
		)

		for index in range(self.list_widget.count()):
			svg_path = self.list_widget.item(index).text()
			svg_to_png_converter(svg_path, output_path, dpi, image_width, image_height)
		self.list_widget.clear()
