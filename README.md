# Advanced Music Player 🎵

An advanced desktop music player built using Python, featuring metadata display, album art, and lyrics fetching capabilities. The player is equipped with intuitive controls for a seamless audio experience.

## Features
- **Play and Control Audio**: Supports MP3, WAV, OGG, and FLAC audio formats.
- **Metadata Display**: Displays song title, artist, and album.
- **Album Art**: Automatically fetches and displays album art if available.
- **Lyrics Fetching**: Fetches and displays song lyrics using an API (e.g., Genius or Musixmatch).
- **Volume Control and Progress Bar**: Adjustable volume and playback progress.
- **User-Friendly UI**: Built with Tkinter for a clean and interactive experience.

## Prerequisites
1. **Python 3.8+** installed on your system.
2. Required Python libraries:
   - `pygame`
   - `mutagen`
   - `Pillow`
   - `requests`
   - `tkinter` (comes with Python)

Install the required libraries using:
```bash
pip install pygame mutagen pillow requests
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/RohitPoul/Advanced-Music-Player.git
   cd Advanced-Music-Player
   ```

2. Run the application:
   ```bash
   python MusicPlayer.py
   ```

## Usage
1. **Open a File**: Click the "Open" button to select an audio file.
2. **Play/Pause**: Use the "Play" button to start playback or pause.
3. **Adjust Volume**: Use the slider to set the desired volume level.
4. **Seek Position**: Drag the progress bar to navigate to a specific part of the song.
5. **View Metadata and Lyrics**: Automatically fetches and displays metadata (title, artist, album) and lyrics.

## Screenshots
![image](https://github.com/user-attachments/assets/75854740-75c0-49a1-92ab-af8f68656a36)
## Lyrics Fetching
The player includes a placeholder for lyrics fetching using an API. You can integrate a lyrics API like Genius or Musixmatch:
- Update the `fetch_lyrics` method in the code with your API key and endpoint.

Example (using Genius API):
```python
def fetch_lyrics(self, title, artist):
    api_url = "https://api.genius.com/search"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    params = {"q": f"{title} {artist}"}
    response = requests.get(api_url, headers=headers, params=params)
    # Extract lyrics from the response
```

## Known Issues
- Album art display depends on the presence of embedded images in the audio metadata.
- Lyrics fetching API integration requires an API key and configuration.

## Contributing
Contributions are welcome! Please fork the repository, create a new branch for your feature or bug fix, and submit a pull request.

## Acknowledgments
- [Pygame](https://www.pygame.org/) for audio playback.
- [Mutagen](https://mutagen.readthedocs.io/) for metadata extraction.
- [Pillow](https://pillow.readthedocs.io/) for image processing.
