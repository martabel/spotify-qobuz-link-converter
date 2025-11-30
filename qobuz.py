import logging
from dotenv import load_dotenv
import os
from qobuz_dl.core import QobuzDL
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

load_dotenv()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    html = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Spotify To Qobuz Link Converter</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f6fa;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: start;
                height: 100vh;
            }

            .container {
                width: 100%;
                max-width: 400px;
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
                color: #333;
            }

            input[type="text"] {
                width: 100%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
                margin-bottom: 15px;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 12px;
                font-size: 16px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.2s;
            }

            button:hover {
                background-color: #357abd;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>Spotify Link</h2>
            <form action="/convert" method="get">
                <input type="text" name="spotify" placeholder="Gib etwas ein..." required>
                <button type="submit">Absenden</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

@app.get("/convert", response_class=HTMLResponse)
def process_input(spotify: str):
    qobuz_link = convert_spotify_to_qobuz(spotify)

    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ergebnis</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f5f6fa;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: start;
                height: 100vh;
            }}

            .result-box {{
                width: 100%;
                max-width: 400px;
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
            }}

            .value {{
                font-size: 20px;
                margin-bottom: 20px;
                color: #333;
            }}

            a {{
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
                padding: 10px 20px;
                background: #4a90e2;
                color: white;
                border-radius: 8px;
            }}

            a:hover {{
                background: #357abd;
            }}
        </style>
    </head>

    <body>
        <div class="result-box">
            <div class="value">Qobuz Link:</div>
            <a class="link" href="{qobuz_link}" target="_blank">{qobuz_link}</a>
            <br><br>
            <a href="/">Zurück</a>
        </div>
    </body>
    </html>
    """
    return html


def convert_spotify_to_qobuz(url):

    match = re.search(r"track/([A-Za-z0-9]+)", url)
    if not match:
        logging.error("Kein Track ID im übergebenen URL gefunden.")
        return "Ungültiger Spotify-Link."
    track_id = match.group(1)
    print("Track ID:", track_id)


    # Lese Credentials aus Umgebungsvariablen
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    qobuz_email = os.getenv("QOBUZ_EMAIL")
    qobuz_password = os.getenv("QOBUZ_PASSWORD")

    missing = []
    if not spotify_client_id:
        missing.append("SPOTIFY_CLIENT_ID")
    if not spotify_client_secret:
        missing.append("SPOTIFY_CLIENT_SECRET")
    if not qobuz_email:
        missing.append("QOBUZ_EMAIL")
    if not qobuz_password:
        missing.append("QOBUZ_PASSWORD")
    if missing:
        msg = f"Fehlende Umgebungsvariablen: {', '.join(missing)}"
        logging.error(msg)
        return msg

    # Auth
    auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Track Daten holen
    track = sp.track(track_id)

    print("Spotify Track Informationen:")
    print("Name:", track["name"])
    print("Artist:", track["artists"][0]["name"])
    print("Album:", track["album"]["name"])
    print("Release date:", track["album"]["release_date"])
    print("Popularity:", track["popularity"])
    print("Preview URL:", track["preview_url"])


    logging.basicConfig(level=logging.INFO)

    qobuz = QobuzDL()
    qobuz.get_tokens() # get 'app_id' and 'secrets' attrs
    qobuz.initialize_client(qobuz_email, qobuz_password, qobuz.app_id, qobuz.secrets)

    print("Qobuz Suche nach dem Spotify Track:")
    q_result = qobuz.search_by_type(track["artists"][0]["name"] + " " + track["name"], "track", limit=1)

    if len(q_result) == 0:
        print("Kein Track auf Qobuz gefunden.")
        return "Kein Track auf Qobuz gefunden."

    return q_result[0]["url"].replace("play", "open")


