import re
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from rich import print


def get_latest_episode_audio(rss: str) -> Path:
    """Downloads the audio file of the latest episode from an RSS feed."""
    print(f"[green]Downloading the latest episode from:[/green] {rss}")

    feed = feedparser.parse(rss)

    # Check if the feed was parsed successfully
    if feed.bozo:
        print("[red]Failed to parse the RSS feed[/red]")
        print(feed.bozo_exception)
        exit(1)

    latest_episode = feed.entries[0]

    audio_url = None
    for link in latest_episode.enclosures:
        if link.type.startswith("audio"):
            audio_url = link.href
            break

    if not audio_url:
        print("[red]No audio file found in the latest episode[/red]")
        exit(1)

    response = requests.get(audio_url)
    if response.status_code != 200:
        print(f"[red]Failed to download the audio file:[/red] {audio_url}")
        print(f"HTTP status code: {response.status_code}")
        exit(1)

    episode_title = latest_episode.title
    pub_date = latest_episode.published_parsed
    pub_date_str = datetime(*pub_date[:6]).strftime("%Y%m%d_%H%M%S")
    sanitized_title = _sanitize_filename(episode_title)
    file_name = f"{pub_date_str}_{sanitized_title}.mp3"

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / file_name

    with file_path.open("wb") as f:
        f.write(response.content)

    return file_path


def _sanitize_filename(filename: str) -> str:
    # Replace any character that is not alphanumeric, a space, or a hyphen with an underscore
    return re.sub(r"[^a-zA-Z0-9\s-]", "_", filename).strip()
