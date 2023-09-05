import os
import subprocess

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QHBoxLayout,
    QFormLayout,
)

from widget_draggable_list import DraggableListWidget
from module_common_utility import get_desktop_path
from module_silence_remover import construct_ffmpeg_command


class SilenceRemoverPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.output_format_label = QLabel("Output Format:", self)
        self.output_format_combobox = QComboBox(self)
        self.output_format_combobox.addItems(["flac", "wav"])
        layout.addWidget(self.output_format_label)
        layout.addWidget(self.output_format_combobox)

        params_layout = QFormLayout()

        self.stop_periods_edit = QLineEdit("-1")
        params_layout.addRow("Stop Periods:", self.stop_periods_edit)

        self.stop_duration_edit = QLineEdit("1")
        params_layout.addRow("Stop Duration:", self.stop_duration_edit)

        self.stop_threshold_edit = QLineEdit("-50dB")
        params_layout.addRow("Stop Threshold:", self.stop_threshold_edit)

        self.detection_edit = QLineEdit("peak")
        params_layout.addRow("Detection:", self.detection_edit)

        layout.addLayout(params_layout)

        self.output_path_label = QLabel("Output Path:", self)
        self.output_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_output_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.output_path_edit)
        path_layout.addWidget(self.browse_button)

        layout.addWidget(self.output_path_label)
        layout.addLayout(path_layout)

        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[
                ".aac",
                ".flac",
                ".m4a",
                ".mp3",
                ".ogg",
                ".opus",
                ".wav",
            ]
        )
        layout.addWidget(self.list_widget)

        self.remove_silence_button = QPushButton("Remove Silence", self)
        self.remove_silence_button.clicked.connect(self.perform_silence_removal)

        layout.addWidget(self.remove_silence_button)
        self.setLayout(layout)

    def browse_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path_edit.setText(directory)

    def perform_silence_removal(self):
        stop_periods = self.stop_periods_edit.text().strip()
        stop_duration = self.stop_duration_edit.text().strip()
        stop_threshold = self.stop_threshold_edit.text().strip()
        detection = self.detection_edit.text().strip()

        params = f"silenceremove=stop_periods={stop_periods}:stop_duration={stop_duration}:stop_threshold={stop_threshold}:detection={detection}"

        output_format = self.output_format_combobox.currentText()
        output_directory = (
            self.output_path_edit.text()
            if self.output_path_edit.text()
            else get_desktop_path()
        )

        for index in range(self.list_widget.count()):
            input_file_path = self.list_widget.item(index).text()

            cmd = construct_ffmpeg_command(
                input_file_path, params, output_format, output_directory
            )

            if os.name == "nt":
                subprocess.run(cmd, shell=True)

        self.list_widget.clear()
