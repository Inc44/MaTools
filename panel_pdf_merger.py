from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from module_pdf_merger import pdf_merger
from widget_draggable_list import DraggableListWidget


class PDFMergerPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.list_widget = DraggableListWidget(accepted_file_extensions=[".pdf"])

        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.merge_pdfs)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.merge_button)
        self.setLayout(layout)

    def merge_pdfs(self):
        pdf_files_to_merge = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        if pdf_files_to_merge:
            pdf_merger(pdf_files_to_merge)
            self.list_widget.clear()
