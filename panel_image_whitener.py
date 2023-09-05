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

        self.compress_button = QPushButton("Whiten")
        self.compress_button.clicked.connect(self.image_whitener)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.compress_button)
        self.setLayout(layout)

    def image_whitener(self):
        png_files_to_process = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        if png_files_to_process:
            image_whitener(png_files_to_process)
            self.list_widget.clear()
