import os
import uuid
from yt_dlp import YoutubeDL

def download_audio(url):
    os.makedirs("downloads", exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join("downloads", filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info["ext"]

    return output_path.replace(".mp3", f".{ext}")
