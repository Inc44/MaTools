import os
from PyQt6.QtWidgets import QListWidget


class DraggableListWidget(QListWidget):
    def __init__(self, accepted_file_extensions=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.accepted_file_extensions = accepted_file_extensions or []

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            for url in mime_data.urls():
                file_path = str(url.toLocalFile())
                if os.path.isdir(file_path):
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if any(
                                full_path.endswith(ext)
                                for ext in self.accepted_file_extensions
                            ):
                                self.addItem(full_path)
                elif any(
                    file_path.endswith(ext) for ext in self.accepted_file_extensions
                ):
                    self.addItem(file_path)
            event.acceptProposedAction()
