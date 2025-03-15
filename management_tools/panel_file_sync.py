from os import walk
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QLineEdit,
	QFileDialog,
	QProgressBar,
	QMessageBox,
	QCheckBox,
)
from module_file_sync import file_sync
from settings_manager import SettingsManager


class FileSyncPanel(QWidget):
	def handle_conflict_gui(
		self,
		file,
		destination_file_size,
		destination_file_date_modified,
		source_file_size,
		source_file_date_modified,
	):
		msg_box = QMessageBox(self)
		msg_box.setWindowTitle("File Conflict")
		msg_box.setText(f"Conflict found for {file}")
		msg_box.setInformativeText(
			f"""
        Source:
        Size: {source_file_size} bytes
        Date: {source_file_date_modified}
        Destination:
        Size: {destination_file_size} bytes
        Date: {destination_file_date_modified}
        Would you like to overwrite the destination file?
        """
		)
		msg_box.setStandardButtons(
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		msg_box.setDefaultButton(QMessageBox.StandardButton.No)
		result = msg_box.exec()
		return "o" if result == QMessageBox.StandardButton.Yes else "s"

	def __init__(self):
		super().__init__()
		self.settings_manager: SettingsManager = SettingsManager()

		self.source_label = QLabel("Source Folder Path:")
		self.source_path_edit = QLineEdit()
		self.source_browse_button = QPushButton("Browse...")
		self.destination_label = QLabel("Destination Folder Path:")
		self.destination_path_edit = QLineEdit()
		self.destination_browse_button = QPushButton("Browse...")
		self.auto_yes_checkbox = QCheckBox("Auto Yes")
		self.detailed_logging_checkbox = QCheckBox("Detailed Logging")
		self.sync_button = QPushButton("Sync")
		self.progress_bar = QProgressBar()

		self.source_browse_button.clicked.connect(self.browse_source)
		self.destination_browse_button.clicked.connect(self.browse_destination)
		self.progress_bar.setValue(0)
		self.sync_button.clicked.connect(self.synchronize)

		source_layout = QHBoxLayout()
		source_layout.addWidget(self.source_path_edit)
		source_layout.addWidget(self.source_browse_button)

		destination_layout = QHBoxLayout()
		destination_layout.addWidget(self.destination_path_edit)
		destination_layout.addWidget(self.destination_browse_button)

		layout = QVBoxLayout()
		layout.addWidget(self.source_label)
		layout.addLayout(source_layout)
		layout.addWidget(self.destination_label)
		layout.addLayout(destination_layout)
		layout.addWidget(self.auto_yes_checkbox)
		layout.addWidget(self.detailed_logging_checkbox)
		layout.addWidget(self.progress_bar)
		layout.addWidget(self.sync_button)

		self.setLayout(layout)

	def browse_source(self):
		"""Open a dialog to select the source folder."""
		folder_path = QFileDialog.getExistingDirectory(self, "Select Source Folder")
		if folder_path:
			self.source_path_edit.setText(folder_path)

	def browse_destination(self):
		"""Open a dialog to select the destination folder."""
		folder_path = QFileDialog.getExistingDirectory(
			self, "Select Destination Folder"
		)
		if folder_path:
			self.destination_path_edit.setText(folder_path)

	def synchronize(self):
		"""Initiate the synchronization process."""
		source_folder = self.source_path_edit.text()
		destination_folder = self.destination_path_edit.text()
		if source_folder and destination_folder:
			total_files = sum(len(files) for _, _, files in walk(source_folder))
		self.processed_files = 0

		def update_progress():
			self.processed_files += 1
			progress = (self.processed_files / total_files) * 100
			red = int(255 * (1 - progress / 100))
			green = int(255 * progress / 100)
			color = QColor(red, green, 0).name()
			self.progress_bar.setValue(int(progress))
			self.progress_bar.setStyleSheet(
				f"QProgressBar::chunk {{ background-color: {color}; }}"
			)
			self.progress_bar.style().unpolish(self.progress_bar)
			self.progress_bar.style().polish(self.progress_bar)

		file_sync(
			source_folder,
			destination_folder,
			callback=update_progress,
			handle_conflict=self.handle_conflict_gui
			if not self.auto_yes_checkbox.isChecked()
			else None,
			auto_yes=self.auto_yes_checkbox.isChecked(),
			detailed_logging=self.detailed_logging_checkbox.isChecked(),
		)
