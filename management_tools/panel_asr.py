from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
)
from module_asr import transcribe
from widget_draggable_list import DraggableListWidget


class AsrPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.setup_output_path_ui(layout)
        self.setup_draggable_list_widget(layout)
        self.setup_convert_button(layout)

        self.setLayout(layout)

    def setup_output_path_ui(self, layout: QVBoxLayout) -> None:
        self.output_path_label = QLabel("Output Path:", self)
        self.output_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_output_path)

        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_button)

    def setup_draggable_list_widget(self, layout: QVBoxLayout) -> None:
        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[".m4a", ".wav", ".flac", ".mp3"]
        )
        layout.addWidget(self.list_widget)

    def setup_convert_button(self, layout: QVBoxLayout) -> None:
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.transcribe_files)
        layout.addWidget(self.convert_button)

    def browse_output_path(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def transcribe_files(self) -> None:
        input_audio_paths = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]

        output_directory_path = self.output_path_edit.text()

        if input_audio_paths:
            for input_audio_path in input_audio_paths:
                transcribe(input_audio_path, output_directory_path)
            self.list_widget.clear()
