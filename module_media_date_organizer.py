"""
Deal with if you have nothing to do:
File Lock (renaming file at the same time)
Renaming already renamed files
Anomaly handling
"""

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Lock
from pathlib import Path
import datetime
import exif
import os
import pyexifinfo as pex
import re
import subprocess
import time
from module_logger import log_info, LogCode

default_media_directories = [
    "Anomaly",
    "EXIF",
    "JPG",
    "PNG",
    "MP4",
    "MOV",
    "M4A",
]

multiprocessing_lock = Lock()


class MediaFile:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.date_time = None

    def update_file_date(self):
        if self.date_time:
            time_stamp = time.mktime(self.date_time.timetuple())
            os.utime(self.file_path, (time_stamp, time_stamp))

    def rename_media_file(self):
        if self.date_time:
            self.file_path = rename_file(self.date_time, self.file_path)

    def rename_media_file(self):
        if self.date_time:
            """
            renamed_file_pattern = re.compile("^\d{8}_\d{6}\.\w+$")
            renamed_existing_file_pattern = re.compile("^\d{8}_\d{6}_\d{3}\.\w+$")
            if renamed_file_pattern.match(self.file_path.stem) or renamed_existing_file_pattern.match(self.file_path.stem):
                log_info(LogCode.ALREADY_RENAMED, file_path=self.file_path)
                return
            else:
                self.file_path = rename_file(self.date_time, self.file_path)
            """
            self.file_path = rename_file(self.date_time, self.file_path)

    def move_to_target_directory(self, target_directory: str):
        with multiprocessing_lock:
            drive_letter = Path(self.file_path).drive.upper()
            if drive_letter != "C:":
                new_path = Path(self.file_path).parent / self.file_path
            else:
                new_path = (
                    Path.home() / "Desktop" / target_directory / self.file_path.name
                )
            if new_path.exists():
                new_path = resolve_naming_conflict(new_path)
            self.file_path.rename(new_path)
            log_info(
                LogCode.FILE_MOVED,
                source_file_path=self.file_path,
                destination_file_path=target_directory,
            )

    def process_exif_data(self):
        self.date_time = date_from_exif(self.file_path)
        return self.date_time

    def process_quicktime_data(self):
        self.date_time = date_from_quicktime_exif(self.file_path)
        return self.date_time

    def process_png_file(self):
        png_ect(self.file_path)

    def process_png_file_name_data(self):
        self.date_time = date_time_from_file_name(self.file_path)
        return bool(self.date_time)


def initialize_workspace():
    for directory in default_media_directories:
        if os.environ["SystemDrive"].upper() == "C:":
            Path(Path.home(), "Desktop", directory).mkdir(exist_ok=True)
        else:
            Path(directory).mkdir(exist_ok=True)


def remove_empty_directories():
    for directory in default_media_directories:
        if os.environ["SystemDrive"].upper() == "C:":
            directory_path = Path(Path.home(), "Desktop", directory)
        else:
            directory_path = Path(directory)
        if directory_path.is_dir() and not any(directory_path.iterdir()):
            directory_path.rmdir()
            log_info(LogCode.DIRECTORY_REMOVED_EMPTY, directory_path=directory_path)


def png_ect(file_path: Path):
    command = f'ect -9 -keep --strict --mt-file "{file_path}"'
    output = subprocess.check_output(command, shell=True, encoding="utf-8")
    striped_output = output.replace("Processed 1 file\n", "").replace("\n", "")
    log_info(LogCode.PNG_ECT, striped_output=striped_output, file_path=file_path)


def date_time_from_file_name(file_path: Path) -> datetime.datetime:
    file_name = os.path.basename(file_path)
    file_name_patterns = [
        (
            r"Screenshot_(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})\.png",
            [0, 1, 2, 3, 4, 5],
        ),
        (
            r"Screenshot_(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-\d+_([\w\.]+)\.jpg",
            [0, 1, 2, 3, 4, 5],
        ),
        (
            r"WhatsApp Image (\d{4})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})\.jpeg",
            [0, 1, 2, 3, 4, 5],
        ),
        (
            r"photo_(\d+)@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})\.jpg",
            [3, 2, 1, 4, 5, 6],
        ),
        (
            r"file_(\d+)@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})\.mp4",
            [3, 2, 1, 4, 5, 6],
        ),
        (
            r"PXL_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{3})\.mp4",
            [0, 1, 2, 3, 4, 5],
        ),
        (r"VID_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.mp4", [0, 1, 2, 3, 4, 5]),
        (
            r"vlcsnap-(\d{4})-(\d{2})-(\d{2})-(\d{2})h(\d{2})m(\d{2})s(\d{3})\.png",
            [0, 1, 2, 3, 4, 5],
        ),
    ]
    for pattern, indices in file_name_patterns:
        match = re.match(pattern, file_name)
        if match:
            year, month, day, hour, minute, second = [
                int(match.group(i + 1)) for i in indices
            ]
            return datetime.datetime(year, month, day, hour, minute, second)
    return None


def date_from_exif(file_path: Path):
    try:
        with open(file_path, "rb") as f:
            tags = exif.Image(f)
    except:
        log_info(LogCode.EXIF_UNPACK_FAILED, file_path=file_path)
        return None
    if not tags.has_exif:
        log_info(LogCode.EXIF_FAILED, file_path=file_path)
        return None
    try:
        if tags.datetime_original == "0000:00:00 00:00:00":
            log_info(LogCode.EXIF_DATETIME_ORIGINAL_EMPTY, file_path=file_path)
            return None
    except:
        log_info(LogCode.EXIF_DATETIME_ORIGINAL_NON_EXISTENT, file_path=file_path)
        return None
    return datetime.datetime.strptime(tags.datetime_original, "%Y:%m:%d %H:%M:%S")


def date_from_quicktime_exif(file_path: Path):
    try:
        data = pex.get_json(str(file_path))
        if data:
            """
            date_tags = [
                "QuickTime:ModifyDate",
                "QuickTime:TrackModifyDate",
                "QuickTime:MediaModifyDate"
            ]
            """
            date_tags = [
                "QuickTime:CreateDate",
                "QuickTime:TrackCreateDate",
                "QuickTime:MediaCreateDate",
            ]
            dates = [data[0].get(tag) for tag in date_tags]
            if len(set(dates)) == 1:
                return datetime.datetime.strptime(dates[0], "%Y:%m:%d %H:%M:%S")
            else:
                log_info(LogCode.QUICKTIME_EXIF_DATES_DIFFER, file_path=file_path)
    except:
        log_info(LogCode.QUICKTIME_EXIF_UNPACK_FAILED, file_path=file_path)
    return None


def update_file_date(datetime_object: datetime, file_path: Path):
    time_stamp = time.mktime(datetime_object.timetuple())
    os.utime(file_path, (time_stamp, time_stamp))


def rename_file(datetime_object: datetime, file_path: Path) -> Path:
    ext = file_path.suffix.lower()
    datename = datetime_object.strftime("%Y%m%d_%H%M%S")
    directory = file_path.parent
    datename = directory / f"{datename}{ext}"
    counter = 1
    while datename.exists() and datename != file_path:
        base, ext = datename.stem, datename.suffix
        new_file = f"{base}_{counter:03d}{ext}"
        datename = directory / new_file
        counter += 1
    file_path.rename(datename)
    return datename


def resolve_naming_conflict(file_path: Path) -> Path:
    counter = 1
    directory, base = file_path.parent, file_path.stem
    ext = file_path.suffix.lower()
    while file_path.exists():
        new_file = f"{base}_{counter:03d}{ext}"
        file_path = directory / new_file
        counter += 1
    return file_path


def fix_file_extension(file_path: Path) -> Path:
    base, ext = file_path.stem, file_path.suffix.lower()
    if ext == ".jpeg":
        ext = ".jpg"
    new_file = base + ext
    new_path = file_path.with_name(new_file)
    file_path.rename(new_path)
    return new_path


def process_media_file(file_path: Path):
    media_file = MediaFile(fix_file_extension(Path(file_path)))
    media_file_extension = media_file.file_path.suffix.lower()
    if media_file_extension in [".mov", ".m4a", ".mp4"]:
        media_file.datetime_object = media_file.process_quicktime_data()
    if media_file_extension in [".jpg", ".png", ".mp4"]:
        media_file.datetime_object = media_file.process_exif_data()
    if not media_file.datetime_object:
        if not media_file.process_png_file_name_data():
            log_info(LogCode.ANOMALY_FOUND, file_path=media_file.file_path)
            # target_directory = "Anomaly"
            return
    extensions = {
        ".png": "PNG",
        ".jpg": "JPG",
        ".mp4": "MP4",
        ".mov": "MOV",
        ".m4a": "M4A",
    }
    if media_file_extension in extensions:
        target_directory = extensions[media_file_extension]
        if media_file_extension == ".png":
            media_file.process_png_file()
    media_file.update_file_date()
    media_file.rename_media_file()
    media_file.move_to_target_directory(target_directory)


def media_date_organizer(files):
    initialize_workspace()
    with ProcessPoolExecutor() as executor:
        executor.map(process_media_file, files)
    remove_empty_directories()
