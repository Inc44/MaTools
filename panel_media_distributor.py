from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
)

from module_media_distributor import organize_files_based_on_naming_pattern
from widget_draggable_list import DraggableListWidget

DESTINATION_PATH_ANIME = r"G:/My Drive/Files/Else/Pictures/Anime"
DESTINATION_PATH_PHOTOS = r"G:/My Drive/Files/Photos"


class MediaDistributorPanel(QWidget):
    """Panel to distribute media files based on naming patterns."""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI components of the panel."""
        layout = QVBoxLayout(self)

        self.add_destination_path_components(layout)

        self.destination_path_label = QLabel("Destination Path:", self)
        self.destination_path_edit = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_destination_path)

        layout.addWidget(self.destination_path_label)
        layout.addWidget(self.destination_path_edit)
        layout.addWidget(self.browse_button)

        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[".png", ".jpg", ".webp", ".tif", ".tiff", ".heic"]
        )
        layout.addWidget(self.list_widget)

        self.organize_button = QPushButton("Organize", self)
        self.organize_button.clicked.connect(self.perform_organization)
        layout.addWidget(self.organize_button)

        self.setLayout(layout)

        self.destination_path_edit.setText(DESTINATION_PATH_PHOTOS)

        self.destination_path_label.hide()
        self.destination_path_edit.hide()
        self.browse_button.hide()

    def add_destination_path_components(self, layout):
        """Add components related to destination path selection."""
        self.add_destination_path_component(
            layout,
            "Select Destination Path:",
            DESTINATION_PATH_PHOTOS,
            DESTINATION_PATH_ANIME,
            "destination_path_dropdown",
        )

    def add_destination_path_component(
        self, layout, label_text, first_path, second_path, dropdown_name
    ):
        """Add a single destination path selection component."""
        label = QLabel(label_text, self)
        dropdown = QComboBox(self)
        dropdown.addItems([first_path, second_path, "Custom..."])
        dropdown.currentTextChanged.connect(self.on_destination_path_changed)
        setattr(self, dropdown_name, dropdown)
        layout.addWidget(label)
        layout.addWidget(dropdown)

    def on_destination_path_changed(self, selected_option):
        """Handle changes in the destination path dropdown."""
        if selected_option == "Custom...":
            self.destination_path_label.show()
            self.destination_path_edit.show()
            self.browse_button.show()
            self.destination_path_edit.clear()  # Clear the path waiting for user input
        else:
            self.destination_path_label.hide()
            self.destination_path_edit.hide()
            self.browse_button.hide()
            self.destination_path_edit.setText(selected_option)

    def browse_destination_path(self):
        """Open a directory browser and set the destination path."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if directory:
            self.destination_path_edit.setText(directory)

    def perform_organization(self):
        """Organize the files based on naming patterns."""
        destination_path = (
            self.destination_path_edit.text().strip()
            if self.destination_path_edit.text().strip()
            else None
        )
        file_paths = [
            self.list_widget.item(index).text()
            for index in range(self.list_widget.count())
        ]
        organize_files_based_on_naming_pattern(destination_path, *file_paths)
        self.list_widget.clear()
