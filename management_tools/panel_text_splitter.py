from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QLabel,
	QPushButton,
	QLineEdit,
	QFileDialog,
	QComboBox,
)
from widget_draggable_list import DraggableListWidget
from module_text_splitter import process_file
from settings_manager import SettingsManager

ACCEPTED_FILE_EXTENSIONS = [".txt"]


class TextSplitterPanel(QWidget):
	def __init__(self):
		super().__init__()
		self.settings_manager = SettingsManager()
		self._initialize_ui_elements()
		self._load_settings()

	def _initialize_ui_elements(self):
		layout = QVBoxLayout(self)

		self.split_type_label = QLabel("Split Type:", self)
		layout.addWidget(self.split_type_label)

		self.split_type_combo = QComboBox(self)
		self.split_type_combo.addItems(["token", "word", "char"])
		layout.addWidget(self.split_type_combo)

		self.amount_label = QLabel("Amount:", self)
		layout.addWidget(self.amount_label)

		self.amount_edit = QLineEdit(self)
		layout.addWidget(self.amount_edit)

		self.amount_edit.textChanged.connect(self._save_settings)

		self.output_path_label = QLabel("Output Folder:", self)
		layout.addWidget(self.output_path_label)

		self.output_path_edit = QLineEdit(self)
		layout.addWidget(self.output_path_edit)

		self.browse_output_button = QPushButton("Browse...", self)
		self.browse_output_button.clicked.connect(self._select_output_path)
		layout.addWidget(self.browse_output_button)

		self.list_widget = DraggableListWidget(
			accepted_file_extensions=ACCEPTED_FILE_EXTENSIONS
		)
		layout.addWidget(self.list_widget)

		self.split_button = QPushButton("Split", self)
		self.split_button.clicked.connect(self._process_file)
		layout.addWidget(self.split_button)

	def _select_output_path(self):
		folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
		if folder:
			self.output_path_edit.setText(folder)

	def _process_file(self):
		split_type = self.split_type_combo.currentText()
		amount = int(self.amount_edit.text())
		output_path = self.output_path_edit.text().strip() or None

		input_paths = [
			self.list_widget.item(index).text()
			for index in range(self.list_widget.count())
		]

		for input_path in input_paths:
			process_file(split_type, amount, input_path, output_path)

		self.list_widget.clear()

	def _load_settings(self):
		amount = self.settings_manager.get_setting("amount")
		if amount:
			self.amount_edit.setText(str(amount))

	def _save_settings(self):
		self.settings_manager.set_setting("amount", self.amount_edit.text())
