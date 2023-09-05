import os
import json
from datetime import datetime


def read_json_file(file_path: str) -> dict:
    """Reads a JSON file and returns its content."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def unix_to_datetime(unix_timestamp: int) -> datetime:
    """Converts a Unix timestamp to a datetime object."""
    return datetime.utcfromtimestamp(int(unix_timestamp))


def construct_full_path(json_path: str, relative_path: str) -> str:
    """Constructs a full path from a base JSON path and a relative path."""
    base_path = os.path.dirname(json_path)
    return os.path.join(base_path, relative_path.replace("/", os.path.sep))


def update_file_date_modified(file_path: str, date_modified: datetime):
    """Updates the date modified of a file."""
    timestamp = date_modified.timestamp()
    os.utime(file_path, (timestamp, timestamp))


def reset_date_modified_to_unix_zero(directory: str):
    """
    Resets the date modified for every file and directory in the provided directory
    and its subdirectories to the Unix timestamp 0 (1970-01-01 00:00:00 UTC).
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.utime(file_path, (0, 0))

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.utime(dir_path, (0, 0))


def process_entry(json_path: str, entry: dict):
    """Processes a single entry from the JSON content."""
    date_modified = unix_to_datetime(entry.get("date_unixtime", 0))

    if "photo" in entry:
        photo_path = construct_full_path(json_path, entry["photo"])
        if os.path.exists(photo_path):
            update_file_date_modified(photo_path, date_modified)

        thumbnail_index = 1
        while True:
            thumbnail_path = construct_full_path(
                json_path, f"{entry['photo']}_thumb.jpg"
            )
            if os.path.exists(thumbnail_path):
                update_file_date_modified(thumbnail_path, date_modified)
                thumbnail_index += 1
            else:
                break

    if "file" in entry:
        file_path = construct_full_path(json_path, entry["file"])
        if os.path.exists(file_path):
            update_file_date_modified(file_path, date_modified)

        if "thumbnail" in entry:
            thumbnail_path = construct_full_path(json_path, entry["thumbnail"])
            if os.path.exists(thumbnail_path):
                update_file_date_modified(thumbnail_path, date_modified)


def telegram_media_date_organizer(json_path: str):
    """Processes the main JSON file."""
    parent_directory = os.path.dirname(json_path)
    reset_date_modified_to_unix_zero(parent_directory)

    json_content = read_json_file(json_path)
    messages_content = json_content.get("messages", [])

    for entry in messages_content:
        process_entry(json_path, entry)
