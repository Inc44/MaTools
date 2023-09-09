import os

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QTimeEdit,
)

from widget_draggable_list import DraggableListWidget
from module_common_utility import get_desktop_path
from module_ffmpeg_video_trim import trim_video


class FFMPEGVideoTrimPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.start_time_label = QLabel("Start Time:", self)
        self.start_time_edit = QTimeEdit(self)
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        layout.addWidget(self.start_time_label)
        layout.addWidget(self.start_time_edit)

        self.end_time_label = QLabel("End Time:", self)
        self.end_time_edit = QTimeEdit(self)
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        layout.addWidget(self.end_time_label)
        layout.addWidget(self.end_time_edit)

        self.output_path_label = QLabel("Output Path:", self)
        self.output_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_output_path)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_button)

        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[".mp4", ".avi", ".mov", ".mkv", ".webm", ".opus"]
        )
        layout.addWidget(self.list_widget)

        self.trim_button = QPushButton("Trim", self)
        self.trim_button.clicked.connect(self.perform_trim)
        layout.addWidget(self.trim_button)
        self.setLayout(layout)

    def browse_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def perform_trim(self):
        start_time = self.start_time_edit.time().toString("HH:mm:ss")
        end_time = self.end_time_edit.time().toString("HH:mm:ss")

        for index in range(self.list_widget.count()):
            input_file_path = self.list_widget.item(index).text()

            output_directory = (
                self.output_path_edit.text()
                if self.output_path_edit.text()
                else get_desktop_path()
            )

            trim_video(input_file_path, start_time, end_time, output_directory)

        self.list_widget.clear()
