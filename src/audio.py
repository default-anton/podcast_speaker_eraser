import platform
import subprocess
from itertools import groupby
from pathlib import Path

from pydub import AudioSegment
from rich import print
from rich.prompt import Prompt

from src.segment import Segment


def select_unwanted_speakers(file_path: Path, segments: list[Segment]) -> list[str]:
    # Extract unique speakers
    unwanted_speakers = []
    segments_by_speaker = groupby(segments, key=lambda s: s.speaker)

    audio = AudioSegment.from_file(file_path)

    for speaker, speaker_segments in segments_by_speaker:
        speaker_segments = list(speaker_segments)
        clip = AudioSegment.empty()
        clip_duration = 0
        for segment in speaker_segments:
            clip += audio[segment.start : segment.end]
            clip_duration += segment.end - segment.start
            if clip_duration >= 10000:
                break

        temp_clip_path = file_path.parent / f"{speaker}_clip.mp3"
        try:
            clip.export(temp_clip_path, format="mp3")

            # Play the audio clip
            if platform.system() == "Darwin":
                subprocess.run(["open", temp_clip_path])
            elif platform.system() == "Windows":
                subprocess.run(["start", temp_clip_path], shell=True)
            elif platform.system() == "Linux":
                subprocess.run(["xdg-open", temp_clip_path])
            else:
                print(
                    f"[red]Unsupported platform:[/red] [bold]{platform.system()}[/bold]"
                )
                break

            response = Prompt.ask(
                "Do you want to delete this speaker? (y/n): ",
                choices=["y", "n"],
                default="n",
            )

            if response == "y":
                unwanted_speakers.append(speaker)
        finally:
            temp_clip_path.unlink(missing_ok=True)

    return unwanted_speakers


def delete_speakers(
    file_path: Path, segments: list[Segment], target_speakers: list[str]
) -> None:
    print(f"[green]Deleting unwanted speakers from:[/green] {file_path}")
    audio = AudioSegment.from_file(file_path)
    result_audio = AudioSegment.empty()
    last_end = 0

    for segment in segments:
        if segment.speaker in target_speakers:
            result_audio += audio[last_end : segment.start]
            last_end = segment.end

    result_audio += audio[last_end:]
    result_audio.export(file_path, format="mp3")
