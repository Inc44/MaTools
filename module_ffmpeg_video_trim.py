import os
import subprocess

from module_common_utility import get_unique_filename


def trim_video(input_file_path, start_time, end_time, output_directory):
    base_filename, file_extension = os.path.splitext(os.path.basename(input_file_path))

    unique_output_filename = get_unique_filename(
        base_filename, file_extension, output_directory
    )
    output_path = os.path.join(output_directory, unique_output_filename)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        input_file_path,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-c",
        "copy",
        output_path,
    ]

    if os.name == "nt":
        subprocess.run(cmd, shell=True)
