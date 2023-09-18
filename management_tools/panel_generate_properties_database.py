from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
)

from module_generate_properties_database import generate_database


class GeneratePropertiesDatabasePanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.input_dir_label = QLabel("Input Directory:", self)
        self.input_dir_edit = QLineEdit(self)
        self.input_browse_button = QPushButton("Browse...", self)
        self.input_browse_button.clicked.connect(self.browse_input_directory)
        layout.addWidget(self.input_dir_label)
        layout.addWidget(self.input_dir_edit)
        layout.addWidget(self.input_browse_button)

        self.output_file_label = QLabel("Output File Path:", self)
        self.output_file_edit = QLineEdit(self)
        self.output_browse_button = QPushButton("Browse...", self)
        self.output_browse_button.clicked.connect(self.browse_output_file)
        layout.addWidget(self.output_file_label)
        layout.addWidget(self.output_file_edit)
        layout.addWidget(self.output_browse_button)

        self.generate_button = QPushButton("Generate Database", self)
        self.generate_button.clicked.connect(self.generate_properties_database)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if directory:
            self.input_dir_edit.setText(directory)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "", "TSV Files (*.tsv);;All Files (*)"
        )
        if file_path:
            self.output_file_edit.setText(file_path)

    def generate_properties_database(self):
        input_directory = self.input_dir_edit.text()
        output_file = (
            self.output_file_edit.text() if self.output_file_edit.text() else None
        )
        generate_database(input_directory, output_file)
