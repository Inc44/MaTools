from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QComboBox,
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

        self.model_label = QLabel("Model:", self)
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(
            ["tiny", "base", "small", "medium", "large", "large-v2"]
        )
        self.model_combo.setCurrentText("large-v2")

        self.language_label = QLabel("Language:", self)
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["en", "fr", "ja", "ru", "uk"])
        self.language_combo.setCurrentText("fr")

        self.device_label = QLabel("Device:", self)
        self.device_combo = QComboBox(self)
        self.device_combo.addItems(["cpu", "cuda"])
        self.device_combo.setCurrentText("cuda")

        self.compute_type_label = QLabel("Compute Type:", self)
        self.compute_type_combo = QComboBox(self)
        self.compute_type_combo.addItems(["int8", "float16", "float32"])
        self.compute_type_combo.setCurrentText("float16")

        self.output_format_label = QLabel("Output Format:", self)
        self.output_format_combo = QComboBox(self)
        self.output_format_combo.addItems(
            ["all", "txt", "srt", "vtt", "tsv", "json", "aud"]
        )
        self.output_format_combo.setCurrentText("txt")

        self.threads_label = QLabel("Threads:", self)
        self.threads_edit = QLineEdit(self)
        self.threads_edit.setText("12")

        self.batch_size_label = QLabel("Batch Size:", self)
        self.batch_size_edit = QLineEdit(self)
        self.batch_size_edit.setText("1")

        self.best_of_label = QLabel("Best Of:", self)
        self.best_of_edit = QLineEdit(self)
        self.best_of_edit.setText("1")

        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_button)

        layout.addWidget(self.model_label)
        layout.addWidget(self.model_combo)

        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)

        layout.addWidget(self.device_label)
        layout.addWidget(self.device_combo)

        layout.addWidget(self.compute_type_label)
        layout.addWidget(self.compute_type_combo)

        layout.addWidget(self.output_format_label)
        layout.addWidget(self.output_format_combo)

        layout.addWidget(self.threads_label)
        layout.addWidget(self.threads_edit)

        layout.addWidget(self.batch_size_label)
        layout.addWidget(self.batch_size_edit)

        layout.addWidget(self.best_of_label)
        layout.addWidget(self.best_of_edit)

    def setup_draggable_list_widget(self, layout: QVBoxLayout) -> None:
        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[".m4a", ".wav", ".flac", ".mp3", ".opus"]
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
        model = self.model_combo.currentText()
        language = self.language_combo.currentText()
        device = self.device_combo.currentText()
        compute_type = self.compute_type_combo.currentText()
        output_format = self.output_format_combo.currentText()
        threads = self.threads_edit.text()
        batch_size = self.batch_size_edit.text()
        best_of = self.best_of_edit.text()
        fp16 = True if compute_type == "float16" else False

        if input_audio_paths:
            for input_audio_path in input_audio_paths:
                transcribe(
                    input_audio_path,
                    output_directory_path,
                    model=model,
                    language=language,
                    device=device,
                    compute_type=compute_type,
                    output_format=output_format,
                    threads=threads,
                    batch_size=batch_size,
                    best_of=best_of,
                    fp16=fp16,
                )
            self.list_widget.clear()
