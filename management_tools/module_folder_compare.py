import hashlib
import os


def compute_file_hash(file_path, algorithm="md5", block_size=4194304):
	"""
	Compute the hash for a given file.

	Parameters:
	- file_path (str): Path to the file
	- algorithm (str): Hash algorithm ('md5', 'sha256', 'sha512'). Default is 'md5'.
	- block_size (int): Block size in bytes. Default is 65536.

	Returns:
	- str: Computed hash for the given file
	"""
	hash_algorithms = {
		"md5": hashlib.md5(),
		"sha256": hashlib.sha256(),
		"sha512": hashlib.sha512(),
	}

	if algorithm not in hash_algorithms:
		raise ValueError(
			f"Unsupported algorithm: {algorithm}. Supported algorithms are 'md5', 'sha256', 'sha512'."
		)

	hasher = hash_algorithms[algorithm]

	with open(file_path, "rb") as file:
		for data in iter(lambda: file.read(block_size), b""):
			hasher.update(data)

	return hasher.hexdigest()


def compare_directories(
	first_directory: str,
	second_directory: str,
	algorithm: str = "md5",
	block_size: int = 4194304,
) -> dict:
	"""Compare two directories based on given parameters.

	Parameters:
	- first_directory (str): Path to the first directory
	- second_directory (str): Path to the second directory
	- algorithm (str): Hash algorithm ('md5', 'sha256', 'sha512')
	- block_size (int): Block size in bytes

	Returns:
	- dict: Results of the comparison
	"""
	results = {
		"not_same_content": [],
		"not_same_date_modified": [],
		"not_same_size": [],
		"bit_rot": [],
	}

	for root, _, files in os.walk(first_directory):
		for file_name in files:
			first_file_path = os.path.join(root, file_name)
			second_file_path = first_file_path.replace(
				first_directory, second_directory
			)

			if not os.path.exists(second_file_path):
				results["not_same_content"].append(
					{"first": first_file_path, "second": None}
				)
				continue

			if os.path.getmtime(first_file_path) != os.path.getmtime(second_file_path):
				results["not_same_date_modified"].append(
					{"first": first_file_path, "second": second_file_path}
				)

			if os.path.getsize(first_file_path) != os.path.getsize(second_file_path):
				results["not_same_size"].append(
					{"first": first_file_path, "second": second_file_path}
				)
				continue

			first_file_hash = compute_file_hash(first_file_path, algorithm, block_size)
			second_file_hash = compute_file_hash(
				second_file_path, algorithm, block_size
			)

			if first_file_hash != second_file_hash:
				if os.path.getsize(first_file_path) == os.path.getsize(
					second_file_path
				):
					results["bit_rot"].append(
						{"first": first_file_path, "second": second_file_path}
					)
				results["not_same_content"].append(
					{"first": first_file_path, "second": second_file_path}
				)

	return results
