from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)
from module_youtube_audio_downloader import YoutubeAudioDownloader

DEFAULT_OUTPUT_PATH = Path.home() / "Desktop"

class YoutubeAudioDownloaderPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.enter_link_label = QLabel("Enter video/playlist yid")
        layout.addWidget(self.enter_link_label)

        self.yid_input = QLineEdit(self)
        layout.addWidget(self.yid_input)

        self.output_path_label = QLabel("Output Path:", self)
        layout.addWidget(self.output_path_label)

        self.output_path_edit = QLineEdit(self)
        layout.addWidget(self.output_path_edit)

        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_output_path)
        layout.addWidget(self.browse_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def browse_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def start_download(self):
        yid = self.yid_input.text().strip()

        output_path = self.output_path_edit.text().strip()
        if not output_path:
            output_path = DEFAULT_OUTPUT_PATH

        downloader = YoutubeAudioDownloader(yid, output_path)
        downloader.run()
