import os
import re
import shutil


def get_file_components(file_name):
    """Extract year, month, and increment from a given file name."""
    pattern = r"(\d{4})(\d{2})\d{2}_\d{6}(_(\d{3}))?\..+"
    match = re.match(pattern, file_name)

    if not match:
        return None, None, None

    year = match.group(1)
    month = match.group(2)
    increment = match.group(4)

    if increment:
        increment = int(increment)
    else:
        increment = 0

    return year, month, increment


def create_destination_folders(base_path, year, month):
    """Create year and year-month folders if they don't exist."""
    year_folder_path = os.path.join(base_path, year)
    year_month_folder_path = os.path.join(year_folder_path, year + month)

    if not os.path.exists(year_month_folder_path):
        os.makedirs(year_month_folder_path)

    return year_month_folder_path


def get_unique_destination_path(year_month_folder_path, file_name, original_increment):
    """Return a unique file path in the destination folder with increment handling."""
    base_name, ext = os.path.splitext(file_name)
    destination_path = os.path.join(year_month_folder_path, file_name)

    increment = original_increment if original_increment > 0 else 1

    while os.path.exists(destination_path):
        if original_increment == 0:
            base_name = base_name + f"_{increment:03}"
            original_increment = 1
        else:
            base_name = base_name.rsplit("_", 1)[0] + f"_{increment:03}"
        file_name = f"{base_name}{ext}"
        destination_path = os.path.join(year_month_folder_path, file_name)
        increment += 1

    return destination_path


def move_or_copy_file(source_path, destination_path):
    """Move or copy the file to the destination based on the drive location."""
    if (
        os.path.splitdrive(source_path)[0].lower()
        != os.path.splitdrive(destination_path)[0].lower()
    ):
        shutil.copy2(source_path, destination_path)
        os.remove(source_path)
    else:
        shutil.move(source_path, destination_path)


def organize_files_based_on_naming_pattern(destination_path, *file_paths):
    """Organize files based on a naming pattern and ensure unique names."""
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        year, month, increment = get_file_components(file_name)

        if year and month:
            year_month_folder_path = create_destination_folders(
                destination_path, year, month
            )
            unique_destination_path = get_unique_destination_path(
                year_month_folder_path, file_name, increment
            )
            move_or_copy_file(file_path, unique_destination_path)
