from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QHBoxLayout,
)

from module_media_distributor import organize_files_based_on_naming_pattern
from widget_draggable_list import DraggableListWidget
from settings_manager import SettingsManager


class MediaDistributorPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.settings_manager: SettingsManager = SettingsManager()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._add_destination_path_components(layout)
        self._add_path_and_browse_to_layout(layout)
        self._add_draggable_list_to_layout(layout)
        self._add_organize_button_to_layout(layout)
        self.setLayout(layout)
        self._hide_path_input_components()

    def _add_destination_path_components(self, layout: QVBoxLayout) -> None:
        path_layout = QHBoxLayout()
        self._populate_destination_path_dropdown(path_layout)
        layout.addLayout(path_layout)

    def _populate_destination_path_dropdown(self, layout: QHBoxLayout) -> None:
        label = QLabel("Select Destination Path:", self)
        dropdown = QComboBox(self)
        dropdown.addItems(self._load_destination_paths() + ["Custom..."])
        dropdown.currentTextChanged.connect(self._handle_destination_path_change)
        self.destination_path_dropdown = dropdown

        self.add_path_button = QPushButton("+", self)
        self.add_path_button.clicked.connect(self._add_current_path_to_settings)
        self.add_path_button.setFixedSize(
            dropdown.sizeHint().height(), dropdown.sizeHint().height()
        )

        self.remove_path_button = QPushButton("-", self)
        self.remove_path_button.clicked.connect(self._remove_current_path_from_settings)
        self.remove_path_button.setFixedSize(
            dropdown.sizeHint().height(), dropdown.sizeHint().height()
        )

        layout.addWidget(label)
        layout.addWidget(dropdown)
        layout.addWidget(self.add_path_button)
        layout.addWidget(self.remove_path_button)

    def _add_path_and_browse_to_layout(self, layout: QVBoxLayout) -> None:
        self.destination_path_label = QLabel("Destination Path:", self)
        self.destination_path_edit = QLineEdit(self)
        self.destination_path_edit.setText(self.destination_path_dropdown.itemText(0))
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self._browse_destination_path)
        layout.addWidget(self.destination_path_label)
        layout.addWidget(self.destination_path_edit)
        layout.addWidget(self.browse_button)

    def _add_draggable_list_to_layout(self, layout: QVBoxLayout) -> None:
        self.list_widget = DraggableListWidget(
            accepted_file_extensions=[".png", ".jpg", ".webp", ".tif", ".tiff", ".heic"]
        )
        layout.addWidget(self.list_widget)

    def _add_organize_button_to_layout(self, layout: QVBoxLayout) -> None:
        self.organize_button = QPushButton("Organize", self)
        self.organize_button.clicked.connect(self._perform_organization)
        layout.addWidget(self.organize_button)

    def _hide_path_input_components(self) -> None:
        self.destination_path_label.hide()
        self.destination_path_edit.hide()
        self.browse_button.hide()

    def _handle_destination_path_change(self, selected_option: str) -> None:
        if selected_option == "Custom...":
            self.destination_path_label.show()
            self.destination_path_edit.show()
            self.browse_button.show()
            self.destination_path_edit.clear()
        else:
            self._hide_path_input_components()
            self.destination_path_edit.setText(selected_option)

    def _browse_destination_path(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if directory:
            self.destination_path_edit.setText(directory)
            self._add_destination_path(directory)

    def _perform_organization(self) -> None:
        destination_path = self.destination_path_edit.text().strip() or None
        file_paths = [
            self.list_widget.item(index).text()
            for index in range(self.list_widget.count())
        ]
        organize_files_based_on_naming_pattern(destination_path, *file_paths)
        self.list_widget.clear()

    def _load_destination_paths(self) -> list[str]:
        return self.settings_manager.get_setting("destination_paths", [])

    def _add_destination_path(self, path: str) -> None:
        paths = self._load_destination_paths()
        if path not in paths:
            paths.append(path)
            self.settings_manager.set_setting("destination_paths", paths)
            self.destination_path_dropdown.addItem(path)

    def _add_current_path_to_settings(self) -> None:
        path = self.destination_path_edit.text().strip()
        if path:
            self._add_destination_path(path)

    def _remove_current_path_from_settings(self) -> None:
        current_path = self.destination_path_dropdown.currentText()
        if current_path and current_path != "Custom...":
            paths = self._load_destination_paths()
            if current_path in paths:
                paths.remove(current_path)
                self.settings_manager.set_setting("destination_paths", paths)
                self.destination_path_dropdown.removeItem(
                    self.destination_path_dropdown.currentIndex()
                )
