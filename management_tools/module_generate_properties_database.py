import csv
import os
from pathlib import Path
from datetime import datetime

DATABASE_NAME = "database_{}.tsv"


def get_file_properties(file_path):
	path_obj = Path(file_path)
	stats = path_obj.stat()
	permissions = oct(stats.st_mode)[-4:]
	return {
		"path": str(path_obj.resolve()),
		"type": "Directory" if path_obj.is_dir() else "File",
		"size_bytes": stats.st_size if path_obj.is_file() else "-",
		"creation_time_unix": stats.st_ctime,
		"modification_time_unix": stats.st_mtime,
		"access_time_unix": stats.st_atime,
		"permissions": permissions,
	}


def save_properties_to_tsv(target_directory, output_filepath):
	with open(output_filepath, "w", newline="", encoding="utf-8") as tsv_file:
		fieldnames = [
			"path",
			"type",
			"size_bytes",
			"creation_time_unix",
			"modification_time_unix",
			"access_time_unix",
			"permissions",
		]
		writer = csv.DictWriter(tsv_file, fieldnames=fieldnames, delimiter="\t")
		writer.writeheader()
		for root, dirs, files in os.walk(target_directory):
			for name in dirs + files:
				full_path = os.path.join(root, name)
				properties = get_file_properties(full_path)
				if properties:
					writer.writerow(properties)


def generate_database(target_directory, output_filepath=None):
	if not output_filepath:
		desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		output_filepath = os.path.join(desktop_path, DATABASE_NAME.format(timestamp))
	save_properties_to_tsv(target_directory, output_filepath)
