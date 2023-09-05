from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)
from widget_draggable_list import DraggableListWidget
from module_ffmpeg_merger import merge_files, get_file_codec


class FFMPEGMergerPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.output_path_label = QLabel("Output Path:", self)
        self.output_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_output_path)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_button)

        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[
                ".aac",
                ".avi",
                ".flac",
                ".m4a",
                ".mkv",
                ".mov",
                ".mp3",
                ".mp4",
                ".ogg",
                ".opus",
                ".wav",
                ".webm",
            ]
        )
        layout.addWidget(self.list_widget)

        self.trim_button = QPushButton("Merge", self)
        self.trim_button.clicked.connect(self.perform_merge)
        layout.addWidget(self.trim_button)
        self.setLayout(layout)

    def browse_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def get_files_from_list_widget(self) -> list:
        """Retrieve the list of files from the DraggableListWidget."""
        return [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]

    def perform_merge(self):
        file_list = self.get_files_from_list_widget()

        output_filepath = merge_files(
            file_list, self.output_path_edit.text(), get_file_codec
        )

        if output_filepath == "Files do not have consistent codecs. Cannot merge.":
            print(output_filepath)
            return

        self.list_widget.clear()
