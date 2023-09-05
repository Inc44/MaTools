from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from module_svg_to_flashcards import process_svg
from widget_draggable_list import DraggableListWidget


class SVGToFlashcardsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.list_widget = DraggableListWidget(accepted_file_extensions=[".svg"])

        self.merge_button = QPushButton("Convert")
        self.merge_button.clicked.connect(self.process_svgs)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.merge_button)
        self.setLayout(layout)

    def process_svgs(self):
        svg_files_to_convert = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        if svg_files_to_convert:
            for svg_file_to_convert in svg_files_to_convert:
                process_svg(svg_file_to_convert)
            self.list_widget.clear()
