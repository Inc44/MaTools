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
        actions = [
            ("File Sync", "icon_file_sync.png", "panel_file_sync", "FileSyncPanel"),
            (
                "Media Date Organizer",
                "icon_media_date_organizer.png",
                "panel_media_date_organizer",
                "MediaDateOrganizerPanel",
            ),
            ("PDF Merger", "icon_pdf_merger.png", "panel_pdf_merger", "PDFMergerPanel"),
            (
                "Python Code Formatter",
                "icon_python_code_formatter.png",
                "panel_python_code_formatter",
                "PythonCodeFormatterPanel",
            ),
            ("Sort Lines", "icon_sort_lines.png", "panel_sort_lines", "SortLinesPanel"),
            (
                "SVG To PNG Converter",
                "icon_svg_to_png_converter.png",
                "panel_svg_to_png_converter",
                "SVGToPNGConverterPanel",
            ),
            (
                "PNG To PDF Converter",
                "icon_png_to_pdf_converter.png",
                "panel_png_to_pdf_converter",
                "PNGToPDFPanel",
            ),
            (
                "Generate Properties Database",
                "icon_generate_properties_database.png",
                "panel_generate_properties_database_compare",
                "GeneratePropertiesDatabasePanel",
            ),
            (
                "Telegram Media Date Organizer",
                "icon_telegram_media_date_organizer.png",
                "panel_telegram_media_date_organizer",
                "TelegramMediaDateOrganizerPanel",
            ),
            (
                "Youtube Audio Downloader",
                "icon_youtube_audio_downloader.png",
                "panel_youtube_audio_downloader",
                "YoutubeAudioDownloaderPanel",
            ),
            (
                "FFMPEG Video Trim",
                "icon_ffmpeg_video_trim.png",
                "panel_ffmpeg_video_trim",
                "FFMPEGVideoTrimPanel",
            ),
            (
                "Image Whitener",
                "icon_image_whitener.png",
                "panel_image_whitener",
                "ImageWhitenerPanel",
            ),
            (
                "Silence Remover",
                "icon_silence_remover.png",
                "panel_silence_remover",
                "SilenceRemoverPanel",
            ),
            (
                "Audio To FLAC Converter",
                "icon_audio_to_flac_converter.png",
                "panel_audio_to_flac_converter",
                "AudioToFLACConverterPanel",
            ),
            (
                "List Subtractor",
                "icon_list_subtractor.png",
                "panel_list_subtractor",
                "ListSubtractorPanel",
            ),
            (
                "Folder Compare",
                "icon_folder_compare.png",
                "panel_folder_compare",
                "FolderComparePanel",
            ),
            (
                "FFMPEG Merger",
                "icon_ffmpeg_merger.png",
                "panel_ffmpeg_merger",
                "FFMPEGMergerPanel",
            ),
            (
                "Audio Duplicate Remover",
                "icon_audio_duplicate_remover.png",
                "panel_audio_duplicate_remover",
                "AudioDuplicateRemoverPanel",
            ),
            (
                "Media Distributor Panel",
                "icon_media_distributor.png",
                "panel_media_distributor",
                "MediaDistributorPanel",
            ),
            #(
                #"SVG To Flashcards Panel",
                #"icon_svg_to_flashcards.png",
                #"panel_svg_to_flashcards",
                #"SVGToFlashcardsPanel",
            #),
        ]

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
