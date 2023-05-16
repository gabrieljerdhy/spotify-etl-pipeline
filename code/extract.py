import json
import os
from datetime import datetime

import boto3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def lambda_handler(event, context):
    cilent_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")

    client_credentials_manager = SpotifyClientCredentials(
        client_id=cilent_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists("spotify")

    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbJVKdmjH0pON?si=6056369be0654082&nd=1"
    playlist_uri = playlist_link.split("/")[-1].split("?")[0]

    spotify_data = sp.playlist_tracks(playlist_uri)

    client = boto3.client("s3")

    filename = "spotify_raw" + str(datetime.now()) + ".json"

    client.put_object(
        Bucket="spotify-etl-project-gab",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data),
    )
