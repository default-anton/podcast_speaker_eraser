import os
import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment

def main() -> None:
    # Load the pre-trained pipeline
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=os.getenv("HUGGINGFACE_ACCESS_TOKEN"),
    )
    pipeline.to(torch.device("mps"))

    # Perform speaker diarization
    with ProgressHook() as progress_hook:
        diarization = pipeline("data/CanadaOrUSA_0_28998.mp3", num_speakers=2, hook=progress_hook)

    # Initialize a list to keep track of segments to keep
    segments_to_keep = []

    # Iterate through the diarization results
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s {speaker}")

        if speaker != "SPEAKER_00":
            start_ms = int(turn.start * 1000)  # Convert to milliseconds
            end_ms = int(turn.end * 1000)      # Convert to milliseconds
            segments_to_keep.append((start_ms, end_ms))

    # Load the audio file using pydub
    audio = AudioSegment.from_file("data/CanadaOrUSA_0_28998.mp3")

    # Create a new AudioSegment object for the modified audio
    modified_audio = AudioSegment.empty()

    # Append segments to keep to the new AudioSegment object
    for start_ms, end_ms in segments_to_keep:
        modified_audio += audio[start_ms:end_ms]

    # Save the modified audio to a new file
    output_path = "data/CanadaOrUSA_0_28998_no_speaker_00.mp3"
    modified_audio.export(output_path, format="mp3")
    print(f"Modified audio saved to {output_path}")

if __name__ == "__main__":
    main()
