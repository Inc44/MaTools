import os
from PIL import Image


def get_directory_from_user():
	"""Get the directory containing the icons from the user."""
	return input("Please enter the directory containing the icons: ")


def get_output_size_from_user():
	"""Get the desired size for one side of the square output image from the user."""
	size = input("Please enter one side of the square output image size: ")
	return int(size)


def resize_and_center_icon(img, size):
	"""Resize and center the icon image in a square of the given size."""
	new_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))

	img_aspect = img.width / img.height
	if img_aspect > 1:
		new_width = size
		new_height = int(size / img_aspect)
	else:
		new_height = size
		new_width = int(size * img_aspect)

	img = img.resize((new_width, new_height), Image.LANCZOS)

	left = (size - new_width) // 2
	top = (size - new_height) // 2

	new_img.paste(img, (left, top))
	return new_img


def process_icons_in_directory(directory, size):
	"""Process each PNG image in the directory."""
	for filename in os.listdir(directory):
		if filename.endswith(".png"):
			filepath = os.path.join(directory, filename)
			img = Image.open(filepath)
			new_img = resize_and_center_icon(img, size)

			new_filepath = os.path.join(directory, f"{size}_{filename}")
			new_img.save(new_filepath)


def main():
	directory = get_directory_from_user()
	size = get_output_size_from_user()
	process_icons_in_directory(directory, size)


if __name__ == "__main__":
	main()
