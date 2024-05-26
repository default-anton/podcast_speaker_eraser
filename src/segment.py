from dataclasses import dataclass
from pathlib import Path
from rich import print


@dataclass
class Segment:
    # Speaker identifier
    speaker: str
    # Start and end times in milliseconds
    start: int
    end: int


def save_segments(episode_path: Path, segments: list[Segment]) -> None:
    print(f"[green]Saving speaker segments to:[/green] {episode_path}")
    with episode_path.with_suffix(".speaker_segments").open("w") as f:
        for segment in segments:
            f.write(f"{segment.speaker},{segment.start},{segment.end}\n")


def load_segments(episode_path: Path) -> list[Segment]:
    segments = []
    try:
        with episode_path.with_suffix(".speaker_segments").open() as f:
            for line in f:
                speaker, start, end = line.strip().split(",")
                segments.append(Segment(speaker, int(start), int(end)))
    except FileNotFoundError:
        pass

    return segments
