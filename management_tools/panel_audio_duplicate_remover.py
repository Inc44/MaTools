import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QFileDialog,
)
from module_audio_duplicate_remover import find_duplicates


class AudioDuplicateRemoverPanel(QWidget):
    """Panel for finding and removing audio duplicates."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout(self)

        self.add_input_path_components(layout)

        self.add_extension_selection_components(layout)

        self.check_button = QPushButton("Check Duplicates", self)
        self.check_button.clicked.connect(self.check_for_duplicates)
        layout.addWidget(self.check_button)

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.remove_button = QPushButton("Remove Duplicates", self)
        self.remove_button.clicked.connect(self.remove_duplicates)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def add_input_path_components(self, layout):
        """Add components related to input path."""
        self.input_path_label = QLabel("Input Path:", self)
        self.input_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_for_input_path)
        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.browse_button)

    def add_extension_selection_components(self, layout):
        """Add components related to extension selection."""
        self.add_extension_component(
            layout, "Keep Extension:", ".flac", ".wav", "keep_extension_dropdown"
        )
        self.add_extension_component(
            layout, "Remove Extension:", ".wav", ".flac", "remove_extension_dropdown"
        )

    def add_extension_component(
        self, layout, label_text, first_item, second_item, dropdown_name
    ):
        """Add a single extension selection component."""
        label = QLabel(label_text, self)
        dropdown = QComboBox(self)
        dropdown.addItems([first_item, second_item])
        setattr(self, dropdown_name, dropdown)
        layout.addWidget(label)
        layout.addWidget(dropdown)

    def browse_for_input_path(self):
        """Open file dialog and update the input path."""
        directory = QFileDialog.getExistingDirectory(self, "Select input Directory")
        if directory:
            self.input_path_edit.setText(directory)

    def check_for_duplicates(self):
        """Check for duplicate audio files."""
        input_path = self.input_path_edit.text()
        keep_extension = self.keep_extension_dropdown.currentText()
        remove_extension = self.remove_extension_dropdown.currentText()

        if not input_path or keep_extension == remove_extension:
            self.result_display.setText(
                "Please provide a valid directory and different extensions."
            )
            return

        self.duplicates = find_duplicates(input_path, keep_extension, remove_extension)
        self.display_found_duplicates()

    def display_found_duplicates(self):
        """Display found duplicate files in the result text area."""
        if self.duplicates:
            result_text = "Duplicate files:\n" + "\n".join(self.duplicates)
            self.result_display.setText(result_text)
        else:
            self.result_display.setText("No duplicate files found.")

    def remove_duplicates(self):
        """Remove the identified duplicate files."""
        if hasattr(self, "duplicates") and self.duplicates:
            for file_path in self.duplicates:
                os.remove(file_path)
            self.result_display.setText("Duplicates removed successfully.")
