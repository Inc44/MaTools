import os
import sys
from functools import partial
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar
from importlib import import_module


def get_script_directory() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def list_python_files(directory_path: str) -> list[str]:
    return [
        file_name[:-3]
        for file_name in sorted(os.listdir(directory_path))
        if file_name.endswith(".py") and file_name.startswith("panel_")
    ]


def generate_class_name(module_name: str) -> str:
    return "".join(word.capitalize() for word in module_name.split("_")) + "Panel"


def generate_icon_name(module_name: str) -> str:
    return f"icon_{module_name}.png"


def generate_tooltip(module_name: str) -> str:
    return module_name.replace("_", " ").title()


def icon_exists(icon_directory: str, icon_name: str) -> bool:
    return os.path.exists(os.path.join(icon_directory, icon_name))


def fetch_actions_from_directory(directory_path: str) -> list[tuple]:
    panel_files = list_python_files(directory_path)
    actions = []

    for panel_name in panel_files:
        element_name = panel_name.replace("panel_", "")
        actions.append(
            (
                generate_tooltip(element_name),
                generate_icon_name(element_name),
                panel_name,
                generate_class_name(element_name),
            )
        )

    return actions


def get_base_path() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return get_script_directory()


def get_icon_path(icon_name: str) -> str:
    return os.path.join(get_base_path(), f"icons/{icon_name}")


def load_stylesheet(theme_name: str) -> str:
    with open(os.path.join(get_base_path(), f"{theme_name}.qss"), "r") as file:
        return file.read()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self) -> None:
        self.setWindowTitle("Management Tools")
        self.setup_toolbar()
        self.setup_default_label()
        self.setup_actions()
        self.set_min_window_width_based_on_toolbar()

    def set_min_window_width_based_on_toolbar(self) -> None:
        toolbar_width = self.toolbar.sizeHint().width()
        self.setMinimumWidth(toolbar_width)

    def show_content(self, module_name: str, class_name: str) -> None:
        module_path = import_module(f"{module_name}")
        panel_class = getattr(module_path, class_name)
        new_panel = panel_class()
        self.setCentralWidget(new_panel)
        recommended_size = new_panel.sizeHint()
        current_size = self.size()
        new_width = max(current_size.width(), recommended_size.width())
        new_height = max(current_size.height(), recommended_size.height())
        self.resize(new_width, new_height)

    def setup_toolbar(self) -> None:
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

    def setup_default_label(self) -> None:
        self.default_label = QLabel("Welcome back to Management Tools", self)
        self.default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.default_label)

    def show_content(self, module_name: str, class_name: str) -> None:
        module_path = import_module(f"{module_name}")
        panel_class = getattr(module_path, class_name)
        self.setCentralWidget(panel_class())

    def setup_actions(self) -> None:
        for tooltip, icon_name, module_name, class_name in fetch_actions_from_directory(
            get_script_directory()
        ):
            action = QAction(QIcon(get_icon_path(icon_name)), "", self)
            action.setToolTip(tooltip)
            action.triggered.connect(
                partial(self.show_content, module_name, class_name)
            )
            self.toolbar.addAction(action)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("white_flat_theme"))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
