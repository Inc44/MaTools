from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton,
	QLabel,
	QLineEdit,
	QFileDialog,
	QCheckBox,
	QGroupBox,
)
from module_ocr import recognize
from widget_draggable_list import DraggableListWidget

LANGUAGES = {
	"eng": "English",
	"fra": "French",
	"jpn": "Japanese",
	"rus": "Russian",
	"ukr": "Ukrainian",
}


class OcrPanel(QWidget):
	def __init__(self) -> None:
		super().__init__()
		self.checkboxes: dict[str, QCheckBox] = {}
		self._initialize_ui()

	def _initialize_ui(self) -> None:
		layout = QVBoxLayout()

		self._setup_dpi_ui(layout)
		self._setup_output_path_ui(layout)
		self._setup_draggable_list_widget(layout)
		self._setup_language_checkboxes(layout)
		self._setup_convert_button(layout)

		self.setLayout(layout)

	def _setup_dpi_ui(self, layout: QVBoxLayout) -> None:
		self.dpi_label = QLabel("DPI:", self)
		self.dpi_edit = QLineEdit(self)
		self.dpi_edit.setText("300")

		layout.addWidget(self.dpi_label)
		layout.addWidget(self.dpi_edit)

	def _setup_output_path_ui(self, layout: QVBoxLayout) -> None:
		self.output_path_label = QLabel("Output Path:", self)
		self.output_path_edit = QLineEdit(self)
		self.browse_button = QPushButton("Browse...", self)

		self.browse_button.clicked.connect(self._browse_output_path)

		layout.addWidget(self.output_path_label)
		layout.addWidget(self.output_path_edit)
		layout.addWidget(self.browse_button)

	def _setup_draggable_list_widget(self, layout: QVBoxLayout) -> None:
		self.list_widget = DraggableListWidget(
			accepted_file_extensions=[".png", ".jpg", ".jpeg", ".pdf"]
		)
		layout.addWidget(self.list_widget)

	def _setup_language_checkboxes(self, layout: QVBoxLayout) -> None:
		language_groupbox = QGroupBox("Languages")
		groupbox_layout = QVBoxLayout()

		for code, name in LANGUAGES.items():
			checkbox = QCheckBox(name)
			checkbox.stateChanged.connect(self.update_checkboxes)
			self.checkboxes[code] = checkbox
			groupbox_layout.addWidget(checkbox)

		language_groupbox.setLayout(groupbox_layout)
		layout.addWidget(language_groupbox)

	def _setup_convert_button(self, layout: QVBoxLayout) -> None:
		self.convert_button = QPushButton("Convert")
		self.convert_button.clicked.connect(self._handle_conversion)

		layout.addWidget(self.convert_button)

	def _browse_output_path(self) -> None:
		directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
		if directory:
			self.output_path_edit.setText(directory)

	def _get_dpi_value(self) -> int:
		return int(self.dpi_edit.text())

	def update_checkboxes(self, _) -> None:
		selected_languages = {
			code for code, checkbox in self.checkboxes.items() if checkbox.isChecked()
		}
		self._handle_language_selection_logic(selected_languages)

	def _handle_language_selection_logic(self, selected_languages: set[str]) -> None:
		self._enable_all_languages()

		if "fra" in selected_languages:
			self._disable_languages(["rus", "ukr", "jpn"])

		if "jpn" in selected_languages:
			self._disable_languages(["fra", "rus", "ukr"])

		if "rus" in selected_languages or "ukr" in selected_languages:
			self._disable_languages(["fra", "jpn"])

	def _disable_languages(self, language_codes: list[str]) -> None:
		for code in language_codes:
			self.checkboxes[code].setEnabled(False)

	def _enable_all_languages(self) -> None:
		for checkbox in self.checkboxes.values():
			checkbox.setEnabled(True)

	def _handle_conversion(self) -> None:
		input_image_paths = [
			self.list_widget.item(i).text() for i in range(self.list_widget.count())
		]
		output_directory_path = self.output_path_edit.text()
		selected_languages = [
			code for code, checkbox in self.checkboxes.items() if checkbox.isChecked()
		]
		dpi_value = self._get_dpi_value()

		if selected_languages:
			for input_image_path in input_image_paths:
				recognize(
					input_image_path,
					output_directory_path,
					selected_languages,
					dpi_value,
				)
			self.list_widget.clear()
