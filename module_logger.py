from pathlib import Path
import logging

logFilePath = Path.home() / "Desktop/results.log"
logging.basicConfig(
    filename=logFilePath, level=logging.INFO, format="%(message)s", encoding="utf-8"
)
log = logging.getLogger(__name__)


class LogCode:
    ALREADY_RENAMED = "ALREADY_RENAMED"
    ANOMALY_FOUND = "ANOMALY_FOUND"
    DIRECTORY_REMOVED = "DIRECTORY_REMOVED"
    DIRECTORY_PERMISSION_DENIED = "DIRECTORY_PERMISSION_DENIED"
    DIRECTORY_REMOVED_EMPTY = "DIRECTORY_REMOVED_EMPTY"
    EXIF_DATETIME_ORIGINAL_EMPTY = "EXIF_DATETIME_ORIGINAL_EMPTY"
    EXIF_DATETIME_ORIGINAL_NON_EXISTENT = "EXIF_DATETIME_ORIGINAL_NON_EXISTENT"
    EXIF_FAILED = "EXIF_FAILED"
    EXIF_UNPACK_FAILED = "EXIF_UNPACK_FAILED"
    FILE_COPIED = "FILE_COPIED"
    FILE_DATE_UPDATED = "FILE_DATE_UPDATED"
    FILE_MODIFIED_DATE_UPDATED = "FILE_MODIFIED_DATE_UPDATED"
    FILE_MOVED = "FILE_MOVED"
    FILE_TYPE_NOT_FOUND = "FILE_TYPE_NOT_FOUND"
    FILE_OVERWRITTEN = "FILE_OVERWRITTEN"
    FILE_REMOVED = "FILE_REMOVED"
    FILE_SKIPPED = "FILE_SKIPPED"
    FILE_UNCHANGED = "FILE_UNCHANGED"
    INVALID_UNIX_TIME = "INVALID_UNIX_TIME"
    JSON_LOAD_DATA_EMPTY = "JSON_LOAD_DATA_EMPTY"
    JSON_LOAD_DATA_FAILED = "JSON_LOAD_DATA_FAILED"
    JSON_SUCCESS = "JSON_SUCCESS"
    MISSING_SOURCE_FILE = "MISSING_SOURCE_FILE"
    NO_FILE_PATH_PROVIDED = "NO_FILE_PATH_PROVIDED"
    PNG_ECT = "PNG_ECT"
    PROCESSING_ERROR = "PROCESSING_ERROR"
    QUICKTIME_EXIF_DATES_DIFFER = "QUICKTIME_EXIF_DATES_DIFFER"
    QUICKTIME_EXIF_UNPACK_FAILED = "QUICKTIME_EXIF_UNPACK_FAILED"
    ROOT_DIR_SUCCESS = "ROOT_DIR_SUCCESS"
    SUBPROCESS_OUTPUT = "SUBPROCESS_OUTPUT"
    UPDATE_DATE_SUCCESS = "UPDATE_DATE_SUCCESS"


LOG_MESSAGES = {
    LogCode.ALREADY_RENAMED: "{file_path}",
    LogCode.ANOMALY_FOUND: "{file_path}",
    LogCode.DIRECTORY_REMOVED: "{directory_path}",
    LogCode.DIRECTORY_PERMISSION_DENIED: "{directory_path}",
    LogCode.DIRECTORY_REMOVED_EMPTY: "{directory_path}",
    LogCode.EXIF_DATETIME_ORIGINAL_EMPTY: "{file_path}",
    LogCode.EXIF_DATETIME_ORIGINAL_NON_EXISTENT: "{file_path}",
    LogCode.EXIF_FAILED: "{file_path}",
    LogCode.EXIF_UNPACK_FAILED: "{file_path}",
    LogCode.FILE_COPIED: "{source_file_path} to {destination_file_path}",
    LogCode.FILE_DATE_UPDATED: "Date of {destination_file_path} ({destination_file_date_modified}) was applied to {source_file_path} ({source_file_date_modified})",
    LogCode.FILE_MODIFIED_DATE_UPDATED: "{source_file_path}: {old_date} to {new_date}",
    LogCode.FILE_MOVED: "{source_file_path} moved to {destination_file_path}",
    LogCode.FILE_TYPE_NOT_FOUND: "{file_type}, {file_path}",
    LogCode.FILE_OVERWRITTEN: "{source_file_path} in {destination_file_path}",
    LogCode.FILE_REMOVED: "{file_path}",
    LogCode.FILE_SKIPPED: "{source_file_path}",
    LogCode.FILE_UNCHANGED: "{source_file_path}",
    LogCode.INVALID_UNIX_TIME: "{file_type}, {file_name}: {date_unixtime}",
    LogCode.JSON_LOAD_DATA_EMPTY: "{file_path}",
    LogCode.JSON_LOAD_DATA_FAILED: "{file_path}: {error}",
    LogCode.JSON_SUCCESS: "{file_path}",
    LogCode.MISSING_SOURCE_FILE: "{destination_file_path}",
    LogCode.NO_FILE_PATH_PROVIDED: "",
    LogCode.PNG_ECT: "{striped_output} for {file_path}",
    LogCode.PROCESSING_ERROR: "{file_type}, {file_path}: {error}",
    LogCode.QUICKTIME_EXIF_DATES_DIFFER: "{file_path}",
    LogCode.QUICKTIME_EXIF_UNPACK_FAILED: "{file_path}",
    LogCode.ROOT_DIR_SUCCESS: "{directory_path}",
    LogCode.SUBPROCESS_OUTPUT: "{stdout}{stderr}",
    LogCode.UPDATE_DATE_SUCCESS: "{file_path} to {modify_timestamp} from {stat}",
}


def log_info(code, **kwargs):
    log.info(f"{code} {LOG_MESSAGES[code].format(**kwargs)}")
