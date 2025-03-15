from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton,
)
from module_image_whitener import image_whitener
from widget_draggable_list import DraggableListWidget


class ImageWhitenerPanel(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		self.list_widget = DraggableListWidget(accepted_file_extensions=[".png"])

		self.whiten_button = QPushButton("Whiten")
		self.whiten_button.clicked.connect(self.whiten_images)

		layout.addWidget(self.list_widget)
		layout.addWidget(self.whiten_button)

		self.setLayout(layout)

	def whiten_images(self):
		image_files_to_whiten = [
			self.list_widget.item(i).text() for i in range(self.list_widget.count())
		]

		if image_files_to_whiten:
			image_whitener(image_files_to_whiten)
			self.list_widget.clear()
