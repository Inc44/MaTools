from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton,
)
from module_telegram_media_date_organizer import telegram_media_date_organizer
from widget_draggable_list import DraggableListWidget


class TelegramMediaDateOrganizerPanel(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		self.list_widget = DraggableListWidget(accepted_file_extensions=[".json"])

		self.process_button = QPushButton("Organize")
		self.process_button.clicked.connect(self.process_json_files)

		layout.addWidget(self.list_widget)
		layout.addWidget(self.process_button)
		self.setLayout(layout)

	def process_json_files(self):
		json_files_to_process = [
			self.list_widget.item(i).text() for i in range(self.list_widget.count())
		]
		for json_file_to_process in json_files_to_process:
			if json_file_to_process:
				telegram_media_date_organizer(json_file_to_process)
		self.list_widget.clear()
