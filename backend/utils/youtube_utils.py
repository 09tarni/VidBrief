from urllib.parse import urlparse, parse_qs


def clean_youtube_url(url: str) -> str:
    """
    Normalize YouTube URLs to standard watch format.
    Fixes youtu.be links and removes extra params.
    """

    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if "v" in query:
        return f"https://www.youtube.com/watch?v={query['v'][0]}"

    return url
