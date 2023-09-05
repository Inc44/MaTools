from typing import List, Tuple, Optional
from xml.etree import ElementTree
from xml.dom.minidom import Node, Document, Element, parseString
import re
from unstable.done_svgcleaner import svgcleaner


BOX_BORDER_COLOR = "#b09cff"


def clone_element(node, doc):
    """Clones an XML DOM Element."""
    new_node = doc.createElement(node.tagName)
    for key, value in node.attributes.items():
        new_node.setAttribute(key, value)

    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            new_node.appendChild(clone_element(child, doc))
        elif child.nodeType == Node.TEXT_NODE:
            new_node.appendChild(doc.createTextNode(child.data))

    return new_node


def parse_path_data(path_element):
    """Extracts path data from the given SVG path element."""
    d = path_element.get("d")
    match = re.search(r"M([\d.]+) ([\d.]+)V([\d.]+)H([\d.]+)V([\d.]+)", d)
    if not match:
        return None
    return map(float, match.groups())


def parse_transform_data(path_element):
    """Parses the transform attribute of the given SVG path element."""
    transform = path_element.get("transform").replace("matrix(", "").replace(")", "")
    return list(map(float, transform.split(",")))


def create_rect_element(
    start_x, start_y, end_x, end_y, scale_y, translate_y, fill, fill_opacity
):
    """Creates and returns an SVG rect element."""
    width = end_x - start_x
    height = start_y - end_y
    transformed_start_y = translate_y + (start_y * scale_y)

    rect_element = ElementTree.Element(
        "rect",
        {
            "width": str(width),
            "height": str(height),
            "x": str(start_x),
            "y": str(transformed_start_y),
            "fill": fill,
            "fill-opacity": str(0),
        },
    )
    return ElementTree.tostring(rect_element).decode()


def path_to_rect(path_element):
    """Converts an SVG path element to an SVG rect element."""
    path_data = parse_path_data(path_element)
    if not path_data:
        return "Invalid path data"

    start_x, start_y, end_y, end_x, _ = path_data
    matrix_values = parse_transform_data(path_element)
    scale_y = matrix_values[3]
    translate_y = matrix_values[5]

    fill = path_element.get("fill", "white")
    fill_opacity = path_element.get("fill-opacity", "1")

    return create_rect_element(
        start_x, start_y, end_x, end_y, scale_y, translate_y, fill, fill_opacity
    )


def replace_paths_with_rects_in_svg(svg_str, fill_color):
    """Replaces all path elements with the specified fill color in the SVG string with rect elements."""
    pattern = re.compile(
        rf'(<path[^>]*?fill="{re.escape(fill_color)}"[^>]*?>)', re.IGNORECASE
    )

    def replacer(match):
        path_str = match.group(1)
        path_elem = ElementTree.fromstring(path_str)
        return path_to_rect(path_elem)

    return re.sub(pattern, replacer, svg_str)


def extract_command_params(path: str) -> List[Tuple[str, List[float]]]:
    """Extract SVG commands and parameters from a path string."""
    commands = re.findall(r"([A-Za-z])([\d. ]+)", path)
    return [
        (command, list(map(float, params.strip().split())))
        for command, params in commands
    ]


def apply_matrix_transform(
    point: Tuple[float, float], matrix_values: str
) -> Tuple[float, float]:
    """Apply matrix transformation to a point."""
    a, b, c, d, e, f = map(float, matrix_values.split(","))
    x, y = point
    return a * x + c * y + e, b * x + d * y + f


def apply_transformations(
    point: Tuple[float, float], transform: Optional[str]
) -> Tuple[float, float]:
    """Apply SVG transformations to a point."""
    if not transform:
        return point

    matrix_values = re.findall(r"matrix\(([^)]+)\)", transform)
    if matrix_values:
        return apply_matrix_transform(point, matrix_values[0])

    return point


def find_single_bounding_box(
    points: List[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    """Find the bounding box for a single list of points."""
    min_x, min_y, max_x, max_y = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )

    for x, y in points:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    return [(min_x, min_y), (max_x, max_y)]


def find_bounding_boxes(
    points_list: List[List[Tuple[float, float]]]
) -> List[List[Tuple[float, float]]]:
    """Find bounding boxes for multiple lists of points."""
    return [find_single_bounding_box(points) for points in points_list]


def create_svg_root(
    document: Document, view_box: str, width: float, height: float
) -> Element:
    """Create the root element for an SVG document."""
    svg_root = document.createElement("svg")
    svg_root.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg_root.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
    svg_root.setAttribute("version", "1.1")
    svg_root.setAttribute("viewBox", view_box)
    svg_root.setAttribute("width", str(width))
    svg_root.setAttribute("height", str(height))
    return svg_root


def create_cropped_svg_document_with_extras(
    bottom_left: Tuple[float, float],
    top_right: Tuple[float, float],
    original_svg_dom: Document,
    extra_elements: List[Element] = [],
) -> Document:
    """Create a new SVG document based on a bounding box and include extra elements."""
    min_x, min_y = bottom_left
    max_x, max_y = top_right
    view_box = f"{min_x} {min_y} {max_x - min_x} {max_y - min_y}"

    new_svg_doc = Document()
    new_svg_root = create_svg_root(new_svg_doc, view_box, max_x - min_x, max_y - min_y)
    new_svg_doc.appendChild(new_svg_root)

    for child in original_svg_dom.documentElement.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            new_svg_root.appendChild(clone_element(child, new_svg_doc))

    for extra_elem in extra_elements:
        new_svg_root.appendChild(clone_element(extra_elem, new_svg_doc))

    return new_svg_doc


def save_single_cropped_svg(svg_doc: Document, file_path: str) -> None:
    """Save a single cropped SVG document to file."""
    with open(file_path, "w") as f:
        f.write(svg_doc.toxml())


def save_cropped_svgs(cropped_svg_docs: List[Document], base_path: str) -> List[str]:
    """Save multiple cropped SVG documents to files."""
    saved_file_paths = []
    for i, svg_doc in enumerate(cropped_svg_docs):
        file_path = f"{base_path}_cropped_{i + 1}.svg"
        save_single_cropped_svg(svg_doc, file_path)
        saved_file_paths.append(file_path)
    return saved_file_paths


def extract_single_rect_border_with_transform(
    width: float, height: float, x: float, y: float, transform: Optional[str] = None
) -> List[Tuple[float, float]]:
    """Extract border coordinates from a single SVG rect element, applying any transformations."""
    corners = [(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)]
    return [apply_transformations(corner, transform) for corner in corners]


def extract_rect_borders_with_transform(
    widths: List[float],
    heights: List[float],
    xs: List[float],
    ys: List[float],
    transforms: List[Optional[str]],
) -> List[List[Tuple[float, float]]]:
    """Extract borders for multiple SVG rect elements."""
    return [
        extract_single_rect_border_with_transform(w, h, x, y, t)
        for w, h, x, y, t in zip(widths, heights, xs, ys, transforms)
    ]


def read_svg_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def parse_svg_dom(svg_content):
    return parseString(svg_content)


def extract_rect_properties(rect_elements, target_color=BOX_BORDER_COLOR):
    widths = []
    heights = []
    xs = []
    ys = []
    transforms = []

    for rect in rect_elements:
        if rect.getAttribute("fill") == target_color:
            widths.append(float(rect.getAttribute("width")))
            heights.append(float(rect.getAttribute("height")))
            xs.append(float(rect.getAttribute("x")))
            ys.append(float(rect.getAttribute("y")))
            transforms.append(rect.getAttribute("transform"))

    return {
        "widths": widths,
        "heights": heights,
        "xs": xs,
        "ys": ys,
        "transforms": transforms,
    }


def save_cropped_svgs(cropped_svg_docs, output_prefix):
    for idx, svg_doc in enumerate(cropped_svg_docs):
        output_path = f"{output_prefix}_{idx}.svg"
        with open(output_path, "w") as f:
            f.write(svg_doc.toxml())


def remove_svg_elements(svg_content: str, tag: str) -> str:
    """
    Remove all elements of a specific tag from an SVG content string.
    """
    pattern = f"<{tag}[^>]*>.*?</{tag}>"
    return re.sub(pattern, "", svg_content, flags=re.DOTALL)


def read_file(file_path: str) -> str:
    """
    Read content from a file and return as a string.
    """
    with open(file_path, "r") as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """
    Write a string content to a file.
    """
    with open(file_path, "w") as f:
        f.write(content)


def svg_compress(input_file_path, output_file_path) -> None:
    """
    Read SVG, remove elements, compress and write back.
    """

    original_svg_content = read_file(input_file_path)

    modified_svg_content = remove_svg_elements(original_svg_content, "text")
    modified_svg_content = remove_svg_elements(original_svg_content, "rect")

    write_file(output_file_path, modified_svg_content)
    svgcleaner(output_file_path, output_file_path)
