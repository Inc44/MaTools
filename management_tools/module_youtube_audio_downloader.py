"""
Specify cookie location (somehow it works)
Fix forbidden 403
"""

from mutagen.flac import Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggopus import OggOpus
from pathlib import Path
import base64
import multiprocessing
import subprocess
import yt_dlp

WORKSPACE_DIRS = ["Production", "Temp"]
INVALID_FILENAME_CHARS = '\/:*?"<>|'
DEFAULT_OUTPUT_PATH = Path.home() / "Desktop"


class YoutubeAudioDownloader:
    class Media:
        def __init__(self, yid, title, upload_date, artist, album, track, release_year):
            self.yid = yid
            self.title = title
            self.upload_date = upload_date
            self.artist = artist
            self.album = album
            self.track = track
            self.release_year = release_year

    def __init__(self, yid, output_path=None):
        self.yid = yid
        self.output_path = Path(output_path) if output_path else DEFAULT_OUTPUT_PATH
        self.output_path.mkdir(parents=True, exist_ok=True)
        self._initialize_workspace()

    def _initialize_workspace(self):
        for dir_name in WORKSPACE_DIRS:
            (self.output_path / dir_name).mkdir(parents=True, exist_ok=True)

    def _create_database(self):
        link = (
            f"https://music.youtube.com/watch?v={self.yid}"
            if len(self.yid) == 11
            else self.yid
        )

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "outtmpl": "%(id)s\x1b%(title)s\x1b%(upload_date)s\x1b%(artist)s\x1b%(album)s\x1b%(track)s\x1b%(release_year)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)

            if "entries" in info:
                data = [ydl.prepare_filename(entry) for entry in info["entries"]]
            else:
                data = [ydl.prepare_filename(info)]

            with open(f"{self.output_path}/main.database", "w", encoding="utf-8") as f:
                f.write("\n".join(data))

    def _read_database(self):
        with open(f"{self.output_path}/main.database", "r", encoding="utf-8") as f:
            for row in map(lambda x: x.split("\x1b"), map(str.strip, f)):
                yield self.Media(*row)

    def _find_extension(self, file_path, extensions, media_type):
        for ext in extensions:
            if (file_path / f"{media_type}.{ext}").is_file():
                return ext
        return None

    def _find_audio_extension(self, mediayid):
        file_path = Path(f"{self.output_path}/Temp/{mediayid}/Audio")
        extensions = ["m4a", "opus", "webm"]
        media_type = "audio"
        return self._find_extension(file_path, extensions, media_type)

    def _find_video_cover_extension(self, mediayid):
        file_path = Path(f"{self.output_path}/Temp/{mediayid}/Cover")
        extensions = ["mp4", "webm"]
        media_type = "video"
        return self._find_extension(file_path, extensions, media_type)

    def _apply_cover(self, media):
        link = f"https://music.youtube.com/watch?v={media.yid}"

        ydl_opts = {
            "quiet": True,
            "format": "bv",
            "outtmpl": f"{self.output_path}/Temp/{media.yid}/Cover/video.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        extc = self._find_video_cover_extension(media.yid)
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                "00:00:00",
                "-i",
                f"{self.output_path}/Temp/{media.yid}/Cover/video.{extc}",
                "-frames:v",
                "1",
                "-q:v",
                "2",
                f"{self.output_path}/Temp/{media.yid}/Cover/cover.png",
                "-y",
            ]
        )
        Path(f"{self.output_path}/Temp/{media.yid}/Cover/video.{extc}").unlink()
        subprocess.run(
            [
                "ect",
                "-quiet",
                "-9",
                "--strict",
                "--mt-file",
                "-keep",
                f"{self.output_path}/Temp/{media.yid}/Cover/cover.png",
            ]
        )
        exta = self._find_audio_extension(media.yid)

        if exta == "m4a":
            self._apply_m4a_cover(media.yid)
        elif exta == "opus":
            self._apply_opus_cover(media.yid)

        Path(f"{self.output_path}/Temp/{media.yid}/Cover/cover.png").unlink()

    def _apply_m4a_cover(self, mediayid):
        with open(
            f"{self.output_path}/Temp/{mediayid}/Cover/cover.png", "rb"
        ) as artwork:
            file = MP4(f"{self.output_path}/Temp/{mediayid}/Audio/audio.m4a")
            file["covr"] = [MP4Cover(artwork.read(), imageformat=MP4Cover.FORMAT_PNG)]
            file.save()

    def _apply_opus_cover(self, mediayid):
        with open(
            f"{self.output_path}/Temp/{mediayid}/Cover/cover.png", "rb"
        ) as artwork:
            file = OggOpus(f"{self.output_path}/Temp/{mediayid}/Audio/audio.opus")
            pic = Picture()
            pic.data = artwork.read()
            pic.type = 3
            pic.mime = "image/png"
            file["metadata_block_picture"] = base64.b64encode(pic.write()).decode(
                "ascii"
            )
            file.save()

    def _ffmpeg(self, media, exta, extf):
        if extf != exta:
            subprocess.run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    f"{self.output_path}/Temp/{media.yid}/Audio/audio.{exta}",
                    "-c:a",
                    "copy",
                    f"{self.output_path}/Temp/{media.yid}/Audio/audio.{extf}",
                    "-y",
                ]
            )
            Path(f"{self.output_path}/Temp/{media.yid}/Audio/audio.{exta}").unlink()

    def _create_playlist(self, medias):
        video_ids = [media.yid for media in medias]
        playlists = [
            ",".join(video_ids[i : i + 50]) for i in range(0, len(video_ids), 50)
        ]
        with open(f"{self.output_path}/main.playlist", "w") as f:
            f.write(
                "\n".join(
                    [
                        f"www.youtube.com/watch_videos?video_ids={ids}"
                        for ids in playlists
                    ]
                )
            )

    def _create_filename(self, media):
        if media.artist != "NA":
            name = f"{media.artist} - {media.album} - {media.track} - {media.release_year} [{media.yid}]"
            name = name.replace(" - NA", "")
        else:
            name = f"{media.title} - {media.upload_date[:4]} [{media.yid}]"
            name = name.replace(" - NA", "")
        name = "".join(c if c not in INVALID_FILENAME_CHARS else "" for c in name)
        if len(name) > 241:
            name = f"{name[:224]}... [{media.yid}]"
        return name

    def _process_file(self, media):
        name = self._create_filename(media)
        link = f"https://music.youtube.com/watch?v={media.yid}"

        ydl_opts = {
            "quiet": True,
            "cookiefile": "cookies.txt",
            "format": "ba",
            "outtmpl": f"{self.output_path}/Temp/{media.yid}/Audio/audio.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        exta = self._find_audio_extension(media.yid)
        extf = "opus" if exta == "webm" else exta
        self._ffmpeg(media, exta, extf)

        if media.artist != "NA":
            self._apply_cover(media)

        Path(f"{self.output_path}/Temp/{media.yid}/Audio/audio.{extf}").rename(
            f"{self.output_path}/Temp/{media.yid}/Audio/{name}.{extf}"
        )
        Path(f"{self.output_path}/Temp/{media.yid}/Audio/{name}.{extf}").replace(
            f"{self.output_path}/Production/{name}.{extf}"
        )

        for directory in [
            f"{self.output_path}/Temp/{media.yid}/Audio",
            f"{self.output_path}/Temp/{media.yid}/Cover",
            f"{self.output_path}/Temp/{media.yid}",
        ]:
            if Path(directory).exists():
                Path(directory).rmdir()

    def run(self):
        multiprocessing.freeze_support()
        self._create_database()
        medias = list(self._read_database())
        self._create_playlist(medias)
        num_processes = min(len(medias), multiprocessing.cpu_count())
        with multiprocessing.Pool(num_processes) as pool:
            pool.map(self._process_file, medias)
        # for media in medias:
        #    self._process_file(media)

        if Path(f"{self.output_path}/Temp").exists():
            Path(f"{self.output_path}/Temp").rmdir()
