import os
from typing import List
from tiktoken import get_encoding
from module_common_utility import get_desktop_path


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.read()


def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(content)


def split_text(text: str, split_type: str, amount: int) -> List[str]:
    if split_type == "token":
        return split_by_tokens(text, amount)
    elif split_type == "word":
        return split_by_words(text, amount)
    elif split_type == "char":
        return split_by_chars(text, amount)
    else:
        raise ValueError(f"Invalid split_type: {split_type}")


def split_by_tokens(text: str, max_tokens: int) -> List[str]:
    encoder = get_encoding("cl100k_base")
    tokens = list(encoder.encode(text))
    chunks = [
        encoder.decode(tokens[start : start + max_tokens])
        for start in range(0, len(tokens), max_tokens)
    ]
    return chunks


def split_by_words(text: str, max_words: int) -> List[str]:
    if not text or max_words <= 0:
        return []

    words = text.split(" ")
    chunks = []

    while words:
        chunk = " ".join(words[:max_words])
        chunks.append(chunk)
        words = words[max_words:]

    return chunks


def split_by_chars(text: str, max_chars: int) -> List[str]:
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def process_file(
    split_type: str, amount: int, input_path: str, output_directory: str = None
) -> None:
    if output_directory is None:
        output_directory = get_desktop_path()

    ensure_directory_exists(output_directory)

    text = read_file(input_path)
    chunks = split_text(text, split_type, amount)
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    for index, chunk in enumerate(chunks):
        output_path = os.path.join(
            output_directory, f"{base_filename}_split_{index}.txt"
        )
        write_to_file(output_path, chunk)


def ensure_directory_exists(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
