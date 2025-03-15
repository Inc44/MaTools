from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QGridLayout
from module_list_subtractor import subtract_lists


class ListSubtractorPanel(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.original_list_title = QLabel("Original")
		self.original_list = QTextEdit()

		self.subtracted_list_title = QLabel("Subtracted")
		self.subtracted_list = QTextEdit()

		self.subtract_button = QPushButton("Subtract Lists")
		self.subtract_button.clicked.connect(self.subtract_and_replace_items)

		self.init_ui()

	def init_ui(self):
		layout = QGridLayout()

		layout.addWidget(self.original_list_title, 0, 0)
		layout.addWidget(self.original_list, 1, 0)
		layout.addWidget(self.subtracted_list_title, 0, 1)
		layout.addWidget(self.subtracted_list, 1, 1)
		layout.addWidget(self.subtract_button, 2, 0, 1, 2)

		self.setLayout(layout)

	def subtract_and_replace_items(self):
		original_text = self.original_list.toPlainText().split("\n")
		subtracted_text = self.subtracted_list.toPlainText().split("\n")

		result = subtract_lists(original_text, subtracted_text)

		self.original_list.setPlainText("\n".join(result))
