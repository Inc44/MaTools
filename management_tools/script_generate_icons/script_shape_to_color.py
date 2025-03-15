from PIL import Image
import os
import numpy as np
from colorsys import rgb_to_hls, hls_to_rgb


def convert_to_rgba(image):
	return image.convert("LA").convert("RGBA")


def initialize_modified_array(image_array_shape):
	return np.zeros(image_array_shape, dtype=np.uint8)


def convert_rgb_to_normalized_hls(rgb_color):
	return rgb_to_hls(rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)


def process_pixel(pixel, target_hls):
	r, g, b, a = pixel
	if r == 0 and g == 0 and b == 0:
		r, g, b = hls_to_rgb(target_hls[0], target_hls[1], target_hls[2])
		r, g, b = int(r * 255), int(g * 255), int(b * 255)
	else:
		lightness = r / 255.0
		inverted_lightness = 1 - lightness
		hue, saturation = target_hls[0], target_hls[2]
		r, g, b = hls_to_rgb(hue, inverted_lightness, saturation)
		r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return r, g, b, a


def apply_color_transformation(image_array, target_hls):
	modified_array = initialize_modified_array(image_array.shape)
	for i, row in enumerate(image_array):
		for j, pixel in enumerate(row):
			modified_array[i, j] = process_pixel(pixel, target_hls)
	return modified_array


def convert_grayscale_alpha_to_color_hsla_inverted(image, target_color=(255, 0, 0)):
	image = convert_to_rgba(image)
	image_array = np.array(image)
	target_hls = convert_rgb_to_normalized_hls(target_color)
	modified_array = apply_color_transformation(image_array, target_hls)
	return Image.fromarray(modified_array, "RGBA")


def create_directory(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)


def get_image_files(directory_path):
	return sorted(f for f in os.listdir(directory_path) if f.lower().endswith(".png"))


def apply_color_transformations(batch_files, colors, image_directory, output_directory):
	for image_file, color in zip(batch_files, colors):
		image_path = os.path.join(image_directory, image_file)
		original_image = Image.open(image_path)

		modified_image = convert_grayscale_alpha_to_color_hsla_inverted(
			original_image, color
		)

		modified_image_path = os.path.join(
			output_directory, f"{os.path.splitext(image_file)[0]}.png"
		)

		modified_image.save(modified_image_path)


def get_input_directory_from_user():
	return input("Please enter the input directory containing the icons: ")


def get_output_directory_from_user():
	return input("Please enter the output directory containing the icons: ")


def main():
	colors = [
		(237, 54, 36),
		(250, 157, 0),
		(47, 218, 119),
		(20, 199, 222),
		(0, 111, 255),
		(68, 79, 173),
		(140, 84, 208),
	]

	image_directory = get_input_directory_from_user()
	output_directory = get_output_directory_from_user()

	create_directory(output_directory)

	image_files = get_image_files(image_directory)

	for i in range(0, len(image_files), 7):
		batch_files = image_files[i : i + 7]
		apply_color_transformations(
			batch_files, colors, image_directory, output_directory
		)


if __name__ == "__main__":
	main()

# safe
