import os
from pathlib import Path

import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from rich import print

from src.segment import Segment


def detect_speakers(file_path: Path) -> list[Segment]:
    """Detect speakers in an audio file and return the segments for each speaker."""
    print(f"[green]Detecting speakers in:[/green] {file_path}")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=os.getenv("HUGGINGFACE_ACCESS_TOKEN"),
    )
    pipeline.to(_torch_device())

    # Perform speaker diarization
    with ProgressHook() as progress_hook:
        diarization = pipeline(str(file_path), hook=progress_hook)

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segment = Segment(
            speaker=speaker, start=int(turn.start * 1000), end=int(turn.end * 1000)
        )
        segments.append(segment)

    return segments


def _torch_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")
