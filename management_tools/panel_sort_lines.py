from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit


class SortLinesPanel(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()

		self.text_input = QTextEdit()
		layout.addWidget(self.text_input)

		self.sort_button = QPushButton("Sort")
		self.sort_button.clicked.connect(self.sort_input_lines)
		layout.addWidget(self.sort_button)

		self.setLayout(layout)

	def sort_input_lines(self):
		lines = self.text_input.toPlainText().split("\n")
		sorted_lines = sorted(lines)
		self.text_input.setPlainText("\n".join(sorted_lines))
