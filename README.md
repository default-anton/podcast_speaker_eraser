# Podcast Speaker Eraser

Podcast Speaker Eraser is a command-line tool designed to help you remove unwanted speakers from podcast episodes. It leverages speaker diarization to detect different speakers in an audio file and allows you to selectively delete segments of audio associated with specific speakers.

## Features

- **Download Latest Episode**: Fetches the latest episode from an RSS feed.
- **Speaker Diarization**: Detects and segments different speakers in the audio file.
- **Interactive Speaker Selection**: Allows you to listen to audio clips of each speaker and choose which ones to delete.
- **Audio Processing**: Removes unwanted speakers from the audio file and saves the cleaned version.

## Future Plans

The end goal for Podcast Speaker Eraser includes the following features:

- **Podcast Management**: Add and manage multiple podcasts.
- **Persistent Speaker Selections**: Remember speaker selections for future episodes of the same podcast.
- **Automated Processing**: Automatically process new episodes based on saved speaker preferences.
- **Custom RSS Feed**: Generate a custom RSS feed with cleaned episodes for each podcast.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/default-anton/podcast_speaker_eraser.git
    cd podcast-speaker-eraser
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - You need a Hugging Face access token to use the speaker diarization model. Set it as an environment variable:
    ```sh
    export HUGGINGFACE_ACCESS_TOKEN=your_huggingface_access_token
    ```

## Usage

To use the Podcast Speaker Eraser, run the following command:
```sh
python main.py <RSS_FEED_URL>
```
Replace `<RSS_FEED_URL>` with the URL of the RSS feed for the podcast you want to process.

Example:
```sh
python main.py https://example.com/podcast/rss
```

## Dependencies

- `pydub`: For audio processing.
- `pyannote.audio`: For speaker diarization.
- `rich`: For rich text formatting in the terminal.
- `feedparser`: For parsing RSS feeds.
- `requests`: For downloading audio files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
