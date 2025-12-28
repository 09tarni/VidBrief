import yt_dlp
import os
import uuid


def download_audio(youtube_url: str) -> str:
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp3",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "retries": 5,
        "fragment_retries": 5,
        "continuedl": False,
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)

        return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
