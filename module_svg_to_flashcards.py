from module_svg_to_flashcards_functions import (
    read_svg_file,
    replace_paths_with_rects_in_svg,
    BOX_BORDER_COLOR,
    parse_svg_dom,
    extract_rect_properties,
    extract_rect_borders_with_transform,
    find_bounding_boxes,
    create_cropped_svg_document_with_extras,
    save_cropped_svgs,
    svg_compress,
)
from module_svg_to_png_converter import svg_to_png_converter


def process_svg(user_svg_path):
    temp_storage = {}

    # Read and modify SVG
    svg_content = read_svg_file(user_svg_path)
    updated_svg_str = replace_paths_with_rects_in_svg(svg_content, BOX_BORDER_COLOR)
    temp_storage["updated_svg"] = updated_svg_str

    # Save updated SVG
    updated_file_path = "res.svg"
    with open(updated_file_path, "w") as f:
        f.write(temp_storage["updated_svg"])

    # Parse SVG DOM
    svg_dom = parse_svg_dom(temp_storage["updated_svg"])
    rect_elements = svg_dom.getElementsByTagName("rect")
    purple_properties = extract_rect_properties(rect_elements)

    # Extract rectangle borders with transformations
    extracted_rect_borders = extract_rect_borders_with_transform(
        purple_properties["widths"],
        purple_properties["heights"],
        purple_properties["xs"],
        purple_properties["ys"],
        purple_properties["transforms"],
    )

    # Find bounding boxes
    bounding_boxes = find_bounding_boxes(extracted_rect_borders)

    # Extract extra elements for cropped SVGs
    clip_elements = svg_dom.getElementsByTagName("clipPath")
    extra_elements = [elem for elem in clip_elements]

    # Create and save cropped SVGs
    cropped_svg_docs = [
        create_cropped_svg_document_with_extras(
            bottom_left, top_right, svg_dom, extra_elements=extra_elements
        )
        for bottom_left, top_right in bounding_boxes
    ]

    save_cropped_svgs(cropped_svg_docs, "res")

    # Generate file paths manually (based on how save_cropped_svgs names files)
    cropped_svg_paths = [f"res_{i}.svg" for i in range(len(bounding_boxes))]

    # TODO to implement
    for i, cropped_svg_path in enumerate(cropped_svg_paths):
        # Compress the SVG file
        compressed_svg_path = f"compressed_res_{i}.svg"
        svg_compress(cropped_svg_path, compressed_svg_path)

        # Convert SVG to PNG
        dpi = 3600
        image_width = None
        image_height = None
        output_dir_path = f"png_output_{i}"
        svg_to_png_converter(
            compressed_svg_path, output_dir_path, dpi, image_width, image_height
        )


if __name__ == "__main__":
    user_svg_path = input("Enter the path to the SVG file: ")
    process_svg(user_svg_path)
