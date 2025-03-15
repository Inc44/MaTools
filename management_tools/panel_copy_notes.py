from PyQt6.QtWidgets import (
	QWidget,
	QLabel,
	QPushButton,
	QGridLayout,
	QLineEdit,
	QVBoxLayout,
	QHBoxLayout,
	QApplication,
)
from settings_manager import SettingsManager


class CopyNotesPanel(QWidget):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)
		self.setup_ui_elements()
		self.init_ui()
		self.name_prompt_dict = {}
		self.load_notes()
		self.populate_ui_with_notes()

	def setup_ui_elements(self) -> None:
		self.name_label = QLabel("Name:")
		self.name_input = QLineEdit()

		self.prompt_label = QLabel("Prompt:")
		self.prompt_input = QLineEdit()

		self.add_button = QPushButton("+")
		self.add_button.clicked.connect(self.add_entry)

		self.remove_button = QPushButton("-")
		self.remove_button.clicked.connect(self.remove_entry)

		self.notes_layout = QVBoxLayout()

	def init_ui(self) -> None:
		layout = QGridLayout()
		layout.addLayout(self.create_name_layout(), 0, 0, 1, 2)
		layout.addLayout(self.create_prompt_layout(), 1, 0, 1, 2)
		layout.addLayout(self.create_button_layout(), 2, 0, 1, 2)
		layout.addLayout(self.notes_layout, 3, 0, 1, 2)
		self.setLayout(layout)

	def create_name_layout(self) -> QHBoxLayout:
		layout = QHBoxLayout()
		layout.addWidget(self.name_label)
		layout.addWidget(self.name_input)
		return layout

	def create_prompt_layout(self) -> QHBoxLayout:
		layout = QHBoxLayout()
		layout.addWidget(self.prompt_label)
		layout.addWidget(self.prompt_input)
		return layout

	def create_button_layout(self) -> QHBoxLayout:
		layout = QHBoxLayout()
		layout.addWidget(self.add_button)
		layout.addWidget(self.remove_button)
		return layout

	def add_name_button(self, name: str) -> None:
		button = QPushButton(name)
		button.clicked.connect(lambda: self.copy_to_clipboard(name))
		self.notes_layout.addWidget(button)

	def remove_name_button(self, name: str) -> None:
		for i in range(self.notes_layout.count()):
			widget = self.notes_layout.itemAt(i).widget()
			if isinstance(widget, QPushButton) and widget.text() == name:
				self.notes_layout.removeWidget(widget)
				widget.setParent(None)
				break

	def copy_to_clipboard(self, name: str) -> None:
		content = f"{self.name_prompt_dict[name]}"
		clipboard = QApplication.clipboard()
		clipboard.setText(content)

	def save_notes(self):
		settings_manager = SettingsManager()
		settings_manager.set_setting("notes", self.name_prompt_dict)

	def load_notes(self):
		settings_manager = SettingsManager()
		self.name_prompt_dict = settings_manager.get_setting("notes", {})

	def populate_ui_with_notes(self):
		for name in self.name_prompt_dict:
			self.add_name_button(name)

	def add_entry(self) -> None:
		name = self.name_input.text()
		prompt = self.prompt_input.text()
		self.name_prompt_dict[name] = prompt
		self.add_name_button(name)
		self.save_notes()

	def remove_entry(self) -> None:
		name_to_remove = self.name_input.text()
		if name_to_remove in self.name_prompt_dict:
			del self.name_prompt_dict[name_to_remove]
			self.remove_name_button(name_to_remove)
			self.save_notes()
