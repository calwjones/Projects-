import time
import json
import hashlib
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials and settings
CLIENT_ID = '0726a201e6f746afa47eb22063f99161'
CLIENT_SECRET = 'eb38eeaa904a49e7ac3efbdf8cff3aa7'
REDIRECT_URI = 'http://localhost:8888/callback'
PLAYLIST_ID = '7IiYMwxKoXoM9YOtodr5fA'
SCOPE = 'playlist-modify-public'

# Create a Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def get_playlist_snapshot():
    """Fetches all tracks from the playlist and returns a hash snapshot and the track list."""
    results = sp.playlist_items(PLAYLIST_ID)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    # Create a list of track IDs
    track_ids = [item.get('track', {}).get('id') for item in tracks if item.get('track')]
    
    # Generate a hash for the snapshot (order doesn't matter here since we sort the IDs)
    snapshot_hash = hashlib.md5(json.dumps(sorted(track_ids)).encode()).hexdigest()
    return snapshot_hash, tracks

def update_playlist_description(tracks):
    """Calculates total duration and updates the playlist description."""
    # Calculate total duration (in milliseconds)
    total_ms = 0
    for item in tracks:
        track = item.get('track')
        if track:
            total_ms += track.get('duration_ms', 0)
    
    # Convert milliseconds into hours, minutes, seconds
    total_seconds = total_ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # Format the description string
    description = f"{hours}hr {minutes}min edge session"
    
    # Update the playlist description
    sp.playlist_change_details(PLAYLIST_ID, description=description)
    print("Playlist description updated!")

# Main loop: take an initial snapshot and check periodically for changes.
last_snapshot = None

while True:
    current_snapshot, tracks = get_playlist_snapshot()
    
    # Compare snapshots; if they differ, update the playlist description.
    if current_snapshot != last_snapshot:
        update_playlist_description(tracks)
        last_snapshot = current_snapshot
    else:
        print("No changes detected.")
    
    # Wait for 60 seconds before checking again (adjust as needed)
    time.sleep(60)
