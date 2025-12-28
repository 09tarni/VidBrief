from pytube import YouTube


def get_video_metadata(url):
    yt = YouTube(url)
    return {
        "title": yt.title,
        "thumbnail": yt.thumbnail_url,
        "length": yt.length
    }
