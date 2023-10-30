import os


def get_files_in_directory(directory_path):
    """
    Retrieve the list of files in the provided directory.

    Parameters:
    - directory_path (str): The path to the directory.

    Returns:
    - list of str: A list of file names in the directory.
    """
    return [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]


def rename_files(directory_path, mapping):
    """
    Rename files in the given directory based on the provided mapping.

    Parameters:
    - directory_path (str): The path to the directory.
    - mapping (dict): A dictionary mapping old file names to new file names.

    Returns:
    - list of str: A list of messages indicating the results of the renaming process.
    """
    files_in_directory = get_files_in_directory(directory_path)
    messages = []

    for old_name in files_in_directory:
        if old_name in mapping:
            new_name = mapping[old_name]
            old_path = os.path.join(directory_path, old_name)
            new_path = os.path.join(directory_path, new_name)

            try:
                os.rename(old_path, new_path)
                messages.append(f"Renamed {old_name} to {new_name}")
            except Exception as e:
                messages.append(f"Error renaming {old_name} to {new_name}: {e}")

    return messages


if __name__ == "__main__":
    DIRECTORY_PATH = input("Enter the directory path: ")
    MAPPING = {
        "01.png": "icon_file_sync.png",
        "02.png": "icon_media_date_organizer.png",
        "03.png": "icon_pdf_merger.png",
        "04.png": "icon_python_code_formatter.png",
        "05.png": "icon_sort_lines.png",
        "06.png": "icon_svg_to_png_converter.png",
        "07.png": "icon_png_to_pdf_converter.png",
        "08.png": "icon_generate_properties_database.png",
        "09.png": "icon_telegram_media_date_organizer.png",
        "10.png": "icon_youtube_audio_downloader.png",
        "11.png": "icon_ffmpeg_video_trim.png",
        "12.png": "icon_image_whitener.png",
        "13.png": "icon_silence_remover.png",
        "14.png": "icon_audio_to_flac_converter.png",
        "15.png": "icon_list_subtractor.png",
        "16.png": "icon_folder_compare.png",
        "17.png": "icon_ffmpeg_merger.png",
        "18.png": "icon_audio_duplicate_remover.png",
        "19.png": "icon_media_distributor.png",
        "20.png": "icon_image_trimmer.png",
        "21.png": "icon_text_splitter.png",
        "22.png": "icon_copy_notes.png",
        "23.png": "icon_ocr.png",
        "24.png": "icon_asr.png",
    }

    results = rename_files(DIRECTORY_PATH, MAPPING)
