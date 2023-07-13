import re
import yt_dlp


def convert_playlist_to_queue(playlist_url, user):
    yt_dl_opts = {
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'quiet': True,
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    playlist_data = ytdl.extract_info(playlist_url, download=False)

    video_urls = []
    for entry in playlist_data['entries']:
        video_urls.append(
            (entry['url'], entry['title'], format_duration(entry['duration']), user))

    return video_urls


def format_duration(duration):
    if duration is None:
        return "0:00"
    hours, remainder = divmod(int(duration), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def is_valid_url(url):
    url_regex = r"^(http|https)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(:[0-9]+)?(/[\w\-\.]*)*(\?[^\s]*)?$"
    return re.match(url_regex, url) is not None
