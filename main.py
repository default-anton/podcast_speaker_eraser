from pathlib import Path

import typer
from rich import print

from src.audio import delete_speakers, select_unwanted_speakers
from src.diarization import detect_speakers
from src.rss import get_latest_episode_audio
from src.segment import Segment, load_segments, save_segments


def main(rss: str) -> None:
    file_path: Path = get_latest_episode_audio(rss)
    segments: list[Segment] = load_segments(file_path)

    if not segments:
        segments = detect_speakers(file_path)
        save_segments(file_path, segments)

    target_speakers = select_unwanted_speakers(file_path, segments)

    if target_speakers:
        delete_speakers(file_path, segments, target_speakers)
        speaker_word = "speakers" if len(target_speakers) > 1 else "speaker"
        print(
            f"[green]Done![/green] Deleted {len(target_speakers)} unwanted {speaker_word} from {file_path}"
        )
    else:
        print("[green]No unwanted speakers found![/green]")


if __name__ == "__main__":
    typer.run(main)
