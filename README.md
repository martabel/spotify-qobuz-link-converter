# Qobuz Link Converter

Small FastAPI tool that takes a Spotify track URL and returns a matching Qobuz link.

The tool:

- extracts the track ID from a Spotify URL
- loads track metadata from the Spotify API
- searches for the track on Qobuz
- returns the resulting Qobuz link in a simple web interface

## Requirements

- Python 3.11 or newer
- Spotify API credentials
- Qobuz account credentials

## Configuration

The application expects a `.env` file in the project root.

Example:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
QOBUZ_EMAIL=your_qobuz_email
QOBUZ_PASSWORD=your_qobuz_password
```

You can use `.env.example` as a template.

## Run Locally

Install dependencies:

```bash
pip install "fastapi>=0.95" "uvicorn[standard]>=0.22" python-dotenv spotipy qobuz-dl
```

Start the server:

```bash
uvicorn qobuz:app --host 0.0.0.0 --port 8000
```

The web interface will then be available at `http://localhost:8000`.

## Run with Docker

Build the image and start the container:

```bash
docker compose up --build
```

The application will then also be available at `http://localhost:8000`.

## Usage

1. Open the start page in your browser.
2. Paste a Spotify track URL.
3. The tool searches Qobuz and displays the resulting link.

You can also call the endpoint directly:

```text
GET /convert?spotify=https://open.spotify.com/track/<TRACK_ID>
```

## Supported Input

The tool currently supports Spotify track URLs only. Other Spotify object types such as album, playlist, or artist URLs are not supported.

## Common Error Messages

- `Ungültiger Spotify-Link.`: No valid track ID could be extracted from the URL.
- `Fehlende Umgebungsvariablen: ...`: One or more required variables are missing from `.env`.
- `Kein Track auf Qobuz gefunden.`: No matching Qobuz result was found for the Spotify track metadata.

## Project Files

- `qobuz.py`: FastAPI app and conversion logic
- `.env.example`: template for required environment variables
- `Dockerfile`: container build for the application
- `docker-compose.yml`: startup via Docker Compose

## Notes

- Do not commit credentials to the repository.
- The Qobuz lookup currently uses a simple `artist + track name` search and returns the first result.
