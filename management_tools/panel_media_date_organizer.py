from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton,
)
from module_media_date_organizer import media_date_organizer
from widget_draggable_list import DraggableListWidget


class MediaDateOrganizerPanel(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		self.list_widget = DraggableListWidget(
			accepted_file_extensions=[".jpg", ".png", ".mov", ".mp4", ".m4a", ".heic"]
		)

		self.process_button = QPushButton("Organize")
		self.process_button.clicked.connect(self.process_media_dates)

		layout.addWidget(self.list_widget)
		layout.addWidget(self.process_button)
		self.setLayout(layout)

	def process_media_dates(self):
		media_files_to_process = [
			self.list_widget.item(i).text() for i in range(self.list_widget.count())
		]
		if media_files_to_process:
			self.process_dates_on_files(media_files_to_process)
			self.list_widget.clear()

	def process_dates_on_files(self, files_list):
		media_date_organizer(files_list)
