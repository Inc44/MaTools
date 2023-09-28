import os
import random
import ctypes
from PIL import Image, ImageDraw, ImageFont
from module_svg_to_png_converter import svg_to_png_converter

PROPORTION = 84
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CONFIG = {
    "FONT_FILE_PATH": os.path.join(
        SCRIPT_DIRECTORY, "fonts/NunitoSans_10pt_SemiCondensed-Bold.ttf"
    ),
    "CITATIONS_FILE_PATH": "G:/My Drive/Files/Else/Notes/Main/Notes/1. Main/2. Citations.md",
    "IDEAS_FILE_PATH": "G:/My Drive/Files/Else/Notes/Main/Notes/1. Main/3. Ideas.md",
    "CITATIONS_AMOUNT": 5,
    "IDEAS_AMOUNT": 0,
    "EMOJI_DIRECTORY": os.path.join(SCRIPT_DIRECTORY, "emojis"),
    "EMOJI_PNG_FILE_NAME": "emoji.png",
    "WALLPAPER_PNG_FILE_NAME": "wallpaper.png",
}


def load_and_sort_text_from_file(file_path: str) -> list:
    """Load and sort text lines from a file."""
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = [line.strip() for line in file if line.strip()]
    return sorted(lines)


def select_random_lines(lines: list, num_lines: int) -> list:
    """Select a random subset of lines."""
    return random.sample(lines, num_lines)


def wrap_text(text: str, char_limit: int) -> str:
    """Wrap text by character limit."""
    words = text.split()
    lines = []
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > char_limit:
            lines.append(line)
            line = ""

        if line:
            line += " " + word
        else:
            line = word

    if line:
        lines.append(line)

    return "\n".join(lines)


def add_padding(text_blocks: list, padding: str = "\n\n") -> str:
    """Add padding between text blocks."""
    return padding.join(block for block in text_blocks if block)


def create_wallpaper(
    citations: list,
    ideas: list,
    emoji_path: str,
    wallpaper_path: str,
    font_path: str,
    image_width: int = 3440, #1920 add auto detect resolution method
    image_height: int = 1440, #1080
    font_size: int = PROPORTION / 2,
    bg_color: str = "black",
    text_color: str = "white",
) -> None:
    """Create a text-based wallpaper."""
    image = Image.new("RGB", (image_width, image_height), color=bg_color)
    font = ImageFont.truetype(font_path, int(font_size))
    draw = ImageDraw.Draw(image)

    wrapped_citations = [wrap_text(citation, PROPORTION) for citation in citations]
    wrapped_ideas = [wrap_text(idea, PROPORTION) for idea in ideas]
    combined_text = add_padding(wrapped_citations + wrapped_ideas)

    text_boundary = draw.multiline_textbbox((0, 0), combined_text, font=font)
    text_width = text_boundary[2] - text_boundary[0]
    text_height = text_boundary[3] - text_boundary[1]

    emoji = Image.open(emoji_path).convert("RGBA")
    emoji_width, emoji_height = emoji.size

    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height - emoji_height * 2) // 2

    draw.multiline_text(
        (text_x, text_y), combined_text, fill=text_color, font=font, align="center"
    )

    emoji_x = (image_width - emoji_width) // 2
    emoji_y = text_y + text_height + emoji_height

    image.paste(emoji, (int(emoji_x), int(emoji_y)), emoji)
    image.save(wallpaper_path)


def set_wallpaper(path: str) -> None:
    """Set wallpaper on a Windows system."""
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)


def select_random_emoji(emoji_dir: str, output_path: str) -> None:
    """Select a random emoji file and convert it to PNG."""
    emoji_list = os.listdir(emoji_dir)
    random_emoji = random.choice(emoji_list)
    random_emoji_path = os.path.join(emoji_dir, random_emoji)

    rendered_path = svg_to_png_converter(
        random_emoji_path,
        output_dir=os.path.dirname(output_path),
        image_width=PROPORTION,
        image_height=PROPORTION,
    )

    os.replace(rendered_path, output_path)


def main() -> None:
    """Main function."""
    temp_dir = (
        os.environ.get("TEMP") or os.environ.get("TMPDIR") or os.environ.get("TMP")
    )

    random_emoji_path = os.path.join(temp_dir, CONFIG["EMOJI_PNG_FILE_NAME"])
    select_random_emoji(CONFIG["EMOJI_DIRECTORY"], random_emoji_path)

    citations = load_and_sort_text_from_file(CONFIG["CITATIONS_FILE_PATH"])
    ideas = load_and_sort_text_from_file(CONFIG["IDEAS_FILE_PATH"])

    selected_citations = select_random_lines(citations, CONFIG["CITATIONS_AMOUNT"])
    selected_ideas = select_random_lines(ideas, CONFIG["IDEAS_AMOUNT"])

    wallpaper_path = os.path.join(temp_dir, CONFIG["WALLPAPER_PNG_FILE_NAME"])

    create_wallpaper(
        selected_citations,
        selected_ideas,
        random_emoji_path,
        wallpaper_path,
        CONFIG["FONT_FILE_PATH"],
    )

    set_wallpaper(wallpaper_path)

    os.remove(wallpaper_path)
    os.remove(random_emoji_path)


if __name__ == "__main__":
    main()
