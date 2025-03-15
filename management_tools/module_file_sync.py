import os
import shutil
from datetime import datetime
from module_logger import log_info, LogCode


def get_file_information(file_path: str) -> tuple:
	"""Retrieve the file size and the date it was last modified."""
	file_stat = os.stat(file_path)
	file_size = file_stat.st_size
	date_modified = datetime.fromtimestamp(file_stat.st_mtime)
	return file_size, date_modified


def compare_file_properties(file1: str, file2: str) -> tuple:
	"""Compare the size and modification date of two files."""
	file1_size, file1_date_modified = get_file_information(file1)
	file2_size, file2_date_modified = get_file_information(file2)
	return file1_size == file2_size, file1_date_modified == file2_date_modified


def handle_conflict_prompt(
	file: str,
	destination_file_size: int,
	destination_file_date_modified: datetime,
	source_file_size: int,
	source_file_date_modified: datetime,
) -> bool:
	"""Handle conflicts by prompting the user."""
	prompt_message = f"""
    Source:
    Size: {source_file_size} bytes
    Date: {source_file_date_modified}
    Destination:
    Size: {destination_file_size} bytes
    Date: {destination_file_date_modified}
    Would you like to overwrite the destination file? (Type 'o' to overwrite)
    """
	user_choice = input(prompt_message)
	return "o" if user_choice.lower() == "o" else "s"


def copy_files_from_source_to_destination(
	source_folder_path,
	destination_folder_path,
	handle_conflict,
	callback,
	auto_yes=False,
	detailed_logging=False,
):
	"""Copy files from the source folder to the destination folder."""
	processed_files = 0
	for dirpath, _, filenames in os.walk(source_folder_path):
		relative_path = os.path.relpath(dirpath, source_folder_path)
		destination_subfolder = os.path.join(destination_folder_path, relative_path)
		if not os.path.exists(destination_subfolder):
			os.makedirs(destination_subfolder)
		for file in filenames:
			source_file_path = os.path.join(dirpath, file)
			destination_file_path = os.path.join(destination_subfolder, file)
			if not os.path.exists(destination_file_path):
				shutil.copy2(source_file_path, destination_file_path)
				if detailed_logging:
					log_info(
						LogCode.FILE_COPIED,
						source_file_path=source_file_path,
						destination_file_path=destination_file_path,
					)

			else:
				source_file_size, source_file_date_modified = get_file_information(
					source_file_path
				)
				(
					destination_file_size,
					destination_file_date_modified,
				) = get_file_information(destination_file_path)
				same_size, same_date = compare_file_properties(
					source_file_path, destination_file_path
				)
				if same_size and same_date:
					"""
                    if detailed_logging:
                        log_info(LogCode.FILE_UNCHANGED,source_file_path=source_file_path)
                    """
				elif same_size and not same_date:
					os.utime(
						source_file_path,
						(
							os.stat(destination_file_path).st_atime,
							os.stat(destination_file_path).st_mtime,
						),
					)
					if detailed_logging:
						log_info(
							LogCode.FILE_DATE_UPDATED,
							source_file_path=source_file_path,
							destination_file_path=destination_file_path,
							source_file_date_modified=source_file_date_modified,
							destination_file_date_modified=destination_file_date_modified,
						)
				else:
					user_choice = handle_conflict(
						file,
						destination_file_size,
						destination_file_date_modified,
						source_file_size,
						source_file_date_modified,
					)
					if user_choice.lower() == "o" or auto_yes:
						shutil.copy2(source_file_path, destination_file_path)
						if detailed_logging:
							log_info(
								LogCode.FILE_OVERWRITTEN,
								source_file_path=source_file_path,
								destination_file_path=destination_file_path,
							)
					else:
						if detailed_logging:
							log_info(
								LogCode.FILE_SKIPPED, source_file_path=source_file_path
							)
			processed_files += 1
			if callback:
				callback()
	return processed_files


def find_folder_differences(source_folder_path, destination_folder_path):
	source_files = []
	destination_files = []
	for dirpath, _, filenames in os.walk(source_folder_path):
		for file in filenames:
			source_files.append(
				os.path.relpath(os.path.join(dirpath, file), source_folder_path)
			)

	for dirpath, _, filenames in os.walk(destination_folder_path):
		for file in filenames:
			destination_files.append(
				os.path.relpath(os.path.join(dirpath, file), destination_folder_path)
			)

	only_in_source = set(source_files) - set(destination_files)
	only_in_destination = set(destination_files) - set(source_files)

	return only_in_source, only_in_destination


def file_sync(
	source_folder_path: str,
	destination_folder_path: str,
	callback=None,
	handle_conflict=None,
	auto_yes=False,
	detailed_logging=False,
) -> None:
	if not handle_conflict:
		handle_conflict = handle_conflict_prompt

	processed_files = copy_files_from_source_to_destination(
		source_folder_path,
		destination_folder_path,
		handle_conflict,
		callback,
		auto_yes=auto_yes,
		detailed_logging=detailed_logging,
	)

	only_in_source, only_in_destination = find_folder_differences(
		source_folder_path, destination_folder_path
	)

	if only_in_source:
		for rel_file in only_in_source:
			destination_file_path = os.path.join(destination_folder_path, rel_file)
			log_info(LogCode.MISSING_DESTINATION_FILE, file_path=destination_file_path)

	if only_in_destination:
		for rel_file in only_in_destination:
			source_file_path = os.path.join(source_folder_path, rel_file)
			log_info(LogCode.MISSING_SOURCE_FILE, file_path=source_file_path)
