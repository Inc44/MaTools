from black import format_str, Mode
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from widget_draggable_list import DraggableListWidget


class PythonCodeFormatterPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.list_widget = DraggableListWidget(accepted_file_extensions=[".py", ".pyw"])

        self.format_button = QPushButton("Format")
        self.format_button.clicked.connect(self.format_python_files)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.format_button)
        self.setLayout(layout)

    def format_python_files(self):
        py_files_to_format = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        for file_path in py_files_to_format:
            with open(file_path, "r", encoding="UTF-8") as f:
                code = f.read()

            formatted_code = format_str(code, mode=Mode())

            with open(file_path, "w", encoding="UTF-8") as f:
                f.write(formatted_code)

        self.list_widget.clear()
