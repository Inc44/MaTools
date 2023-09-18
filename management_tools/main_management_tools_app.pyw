import os
import sys
from functools import partial
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QToolBar,
)
from importlib import import_module


def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))


def list_python_files(directory_path):
    return [
        f[:-3]
        for f in os.listdir(directory_path)
        if f.endswith(".py") and f.startswith("panel_")
    ]


def generate_class_name(module_name):
    return "".join(word.capitalize() for word in module_name.split("_")) + "Panel"


def generate_icon_name(module_name):
    return f"icon_{module_name}.png"


def generate_tooltip(module_name):
    return module_name.replace("_", " ").title()


def generate_panel_name(module_name):
    return f"{module_name}"


def icon_exists(icon_directory, icon_name):
    return os.path.exists(os.path.join(icon_directory, icon_name))


def fetch_actions_from_directory(directory_path):
    panel_files = list_python_files(directory_path)
    actions = []

    for panel_name in panel_files:
        element_name = panel_name.replace("panel_", "")
        class_name = generate_class_name(element_name)
        icon_name = generate_icon_name(element_name)
        tooltip = generate_tooltip(element_name)
        actions.append((tooltip, icon_name, panel_name, class_name))

    return actions


def get_base_path() -> str:
    """
    Return the base path for the application.
    If the application is bundled using PyInstaller, return the path of the app.
    Otherwise, return the directory of this script.
    """
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_icon_path(icon_name: str) -> str:
    """
    Return the complete path for the given icon name.
    """
    return os.path.join(get_base_path(), f"icons/{icon_name}")


def load_stylesheet(theme_name: str) -> str:
    """
    Load the stylesheet from a qss file based on the theme name.
    """
    base_path = get_base_path()
    with open(os.path.join(base_path, f"{theme_name}.qss"), "r") as file:
        return file.read()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Management Tools")

        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.default_label = QLabel("Welcome back to Management Tools", self)
        self.default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.default_label.setObjectName("defaultLabel")
        self.setCentralWidget(self.default_label)

        self.setup_actions()

    def show_content(self, module_name: str, class_name: str):
        """
        Imports the specified module, instantiates the specified class from that module,
        and sets it as the central widget.
        """
        module_path = import_module(f"{module_name}")
        panel_class = getattr(module_path, class_name)
        self.setCentralWidget(panel_class())

    def setup_actions(self):
        directory_path = get_script_directory()
        actions = fetch_actions_from_directory(directory_path)

        for tooltip, icon_name, module_name, class_name in actions:
            action = QAction(QIcon(get_icon_path(icon_name)), "", self)
            action.setToolTip(tooltip)
            callback = partial(self.show_content, module_name, class_name)
            action.triggered.connect(callback)
            self.toolbar.addAction(action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme_name = "white_flat_theme"
    app.setStyleSheet(load_stylesheet(theme_name))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
