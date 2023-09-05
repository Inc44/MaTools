from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QPlainTextEdit,
)
from module_folder_compare import compare_directories


class FolderComparePanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.first_dir_label = QLabel("First Directory:", self)
        self.first_dir_edit = QLineEdit(self)
        self.first_browse_button = QPushButton("Browse...", self)
        self.first_browse_button.clicked.connect(self.browse_first_directory)
        layout.addWidget(self.first_dir_label)
        layout.addWidget(self.first_dir_edit)
        layout.addWidget(self.first_browse_button)

        self.second_dir_label = QLabel("Second Directory:", self)
        self.second_dir_edit = QLineEdit(self)
        self.second_browse_button = QPushButton("Browse...", self)
        self.second_browse_button.clicked.connect(self.browse_second_directory)
        layout.addWidget(self.second_dir_label)
        layout.addWidget(self.second_dir_edit)
        layout.addWidget(self.second_browse_button)

        algo_layout = QHBoxLayout()
        self.algorithm_label = QLabel("Algorithm:", self)
        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItems(["md5", "sha256", "sha512"])
        algo_layout.addWidget(self.algorithm_label)
        algo_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algo_layout)

        self.compare_button = QPushButton("Compare", self)
        self.compare_button.clicked.connect(self.perform_comparison)
        layout.addWidget(self.compare_button)

        self.results_display = QPlainTextEdit(self)
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        self.setLayout(layout)

    def browse_first_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select First Directory")
        if directory:
            self.first_dir_edit.setText(directory)

    def browse_second_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Second Directory")
        if directory:
            self.second_dir_edit.setText(directory)

    def perform_comparison(self):
        first_dir = self.first_dir_edit.text()
        second_dir = self.second_dir_edit.text()
        algorithm = self.algorithm_combo.currentText()

        results = compare_directories(first_dir, second_dir, algorithm)

        results_text = self.format_comparison_results(results)

        self.results_display.setPlainText(results_text)

    def format_comparison_results(self, results):
        """Helper function to format the comparison results for display."""
        results_text = ""
        for category, file_dicts in results.items():
            results_text += f"{category}:\n"
            for file_dict in file_dicts:
                if file_dict.get("second"):
                    results_text += (
                        f"First: {file_dict['first']} | Second: {file_dict['second']}\n"
                    )
                else:
                    results_text += (
                        f"Missing in second directory: {file_dict['first']}\n"
                    )
            results_text += "\n\n"
        return results_text
