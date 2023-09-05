import os
from module_common_utility import get_unique_filename


def construct_ffmpeg_command(input_file_path, params, output_format, output_directory):
    base_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    unique_output_filename = get_unique_filename(
        base_filename, f".{output_format}", output_directory
    )
    output_path = os.path.join(output_directory, unique_output_filename)

    cmd = [
        "ffmpeg",
        "-i",
        input_file_path,
        "-af",
        params,
        output_path,
    ]

    if output_format == "flac":
        cmd.extend(["-compression_level", "12"])

    return cmd
