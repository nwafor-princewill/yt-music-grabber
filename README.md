# YT Music Grabber

A local web tool to download YouTube Music tracks as MP3 with album art and metadata.

## Features
- No ads, no tracking, completely local
- Downloads as MP3, MP4, or WEBM
- Embeds cover art and artist name (via yt-dlp + ffmpeg)
- Clean, modern UI

## Requirements
- Python 3.7+
- FFmpeg (added to PATH)

## Setup
1. Clone the repo.
2. Install dependencies: `pip install flask flask-cors yt-dlp`
3. Set correct FFmpeg path in `app.py`.
4. Run `python app.py` and `python -m http.server 5501`.
5. Open `http://localhost:5501`.

## How to Use
Paste a YouTube/YouTube Music link, choose format, click "GRAB MUSIC". The file will download to your PC with full metadata.

## Disclaimer
Pay 500 naira a month to enjoy seamless and uninterrupted music with no ads enjoy..