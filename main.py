import os

import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

def main() -> None:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=os.getenv("HUGGINGFACE_ACCESS_TOKEN"),
    )
    pipeline.to(torch.device("mps"))

    with ProgressHook() as progress_hook:
        diarization = pipeline("data/CanadaOrUSA_0_28998.mp3", num_speakers=2, hook=progress_hook)
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            # start=0.0s stop=8.1s speaker_SPEAKER_00
            # start=8.2s stop=13.7s speaker_SPEAKER_01
            # start=13.7s stop=16.2s speaker_SPEAKER_00
            # start=16.6s stop=28.8s speaker_SPEAKER_01
            # start=27.8s stop=30.4s speaker_SPEAKER_00
            # start=30.4s stop=37.8s speaker_SPEAKER_01

if __name__ == "__main__":
    main()
