from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from module_image_trimmer import path_images_trimmer
from widget_draggable_list import DraggableListWidget

class ImageTrimmerPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.list_widget = DraggableListWidget(accepted_file_extensions=[".png"])

        self.trim_button = QPushButton("Trim")
        self.trim_button.clicked.connect(self.trim_images)
        
        layout.addWidget(self.list_widget)
        layout.addWidget(self.trim_button)
        
        self.setLayout(layout)

    def trim_images(self):
        image_files_to_trim = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        
        if image_files_to_trim:
            path_images_trimmer(image_files_to_trim)
            self.list_widget.clear()
