from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)

from module_audio_to_flac_converter import convert_audio_to_flac_parallel
from widget_draggable_list import DraggableListWidget


ACCEPTED_FILE_EXTENSIONS = [
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
    ".mkv",
]


class AudioToFLACConverterPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._initialize_ui_elements()

    def _initialize_ui_elements(self):
        layout = QVBoxLayout(self)

        self.output_path_label = QLabel("Output Path:", self)
        layout.addWidget(self.output_path_label)

        self.output_path_edit = QLineEdit(self)
        layout.addWidget(self.output_path_edit)

        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self._select_output_path)
        layout.addWidget(self.browse_button)

        self.list_widget = DraggableListWidget(
            accepted_file_extensions=ACCEPTED_FILE_EXTENSIONS
        )
        layout.addWidget(self.list_widget)

        self.compress_button = QPushButton("Compress", self)
        self.compress_button.clicked.connect(self._compress_audio_files)
        layout.addWidget(self.compress_button)

    def _select_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def _compress_audio_files(self):
        output_path = self.output_path_edit.text().strip() or None
        audio_paths = [
            self.list_widget.item(index).text()
            for index in range(self.list_widget.count())
        ]

        convert_audio_to_flac_parallel(audio_paths, output_directory=output_path)
        self.list_widget.clear()
