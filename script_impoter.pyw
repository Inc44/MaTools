from pathlib import Path
import glob
import subprocess
from module_logger import log_info, LogCode


def move_to_target_directory(source_file_path: Path) -> None:
    """Move the given file to the target directory and log the action."""
    target_directory = Path.home() / "Desktop" / "Imported"
    destination_file_path = target_directory / source_file_path.name
    counter = 1
    while destination_file_path.exists():
        base_name, extension = source_file_path.stem, source_file_path.suffix
        new_file_name = f"{base_name}_{counter:03d}{extension}"
        destination_file_path = target_directory / new_file_name
        counter += 1
    source_file_path.rename(destination_file_path)
    log_info(
        LogCode.FILE_MOVED,
        source_file_path=source_file_path,
        destination_file_path=destination_file_path,
    )


def remove_empty_subfolders(directory_path: Path) -> None:
    """Remove empty subfolders from the given directory and log the action."""
    for subdirectory_path in directory_path.glob("**/*"):
        try:
            if subdirectory_path.is_dir() and not any(subdirectory_path.iterdir()):
                subdirectory_path.rmdir()
                log_info(
                    LogCode.DIRECTORY_REMOVED,
                    directory_path=subdirectory_path,
                )
        except PermissionError:
            log_info(
                LogCode.DIRECTORY_PERMISSION_DENIED,
                directory_path=subdirectory_path,
            )


def execute_command(command_str: str) -> tuple:
    """Execute the given shell command and return stdout and stderr."""
    process = subprocess.run(
        command_str,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return process.stdout, process.stderr


def main():
    stdout, stderr = execute_command("adb devices")
    log_info(
        LogCode.SUBPROCESS_OUTPUT,
        stdout=stdout,
        stderr=stderr,
    )

    source_directories = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures/Screenshots",
    ]
    destination_directory = Path.home() / "Pictures"

    for source_directory in source_directories:
        stdout, stderr = execute_command(
            f"adb pull -a {source_directory} {destination_directory}"
        )
        log_info(
            LogCode.SUBPROCESS_OUTPUT,
            stdout=stdout,
            stderr=stderr,
        )

    target_directory = Path.home() / "Desktop" / "Imported"
    target_directory.mkdir(exist_ok=True)
    files = [
        Path(path)
        for path in glob.glob(f"{destination_directory}/**/*", recursive=True)
        if Path(path).is_file() and destination_directory.exists()
    ]
    for file_path in files:
        move_to_target_directory(file_path)

    remove_empty_subfolders(destination_directory)
    for source_directory in source_directories:
        ls_process = subprocess.run(
            f"adb shell ls {source_directory}",
            shell=True,
            capture_output=True,
            encoding="utf-8",
        )
        files_to_export = []
        if ls_process.returncode == 0:
            files_to_export = ls_process.stdout.splitlines()
        imported_files = [
            file.name for file in target_directory.iterdir() if file.is_file()
        ]
        for file in files_to_export:
            if file in imported_files:
                file_path = Path(source_directory) / file
                stdout, stderr = execute_command(f"adb shell rm {file_path}")
                log_info(
                    LogCode.FILE_REMOVED,
                    file_path=file_path,
                )


if __name__ == "__main__":
    main()
