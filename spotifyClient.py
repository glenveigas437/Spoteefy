import json
import requests
from track import Track
from playlist import Playlist


class SpotifyClient:
    
    def __init__(self, authorization_token, user_id):
        self._authorization_token = authorization_token
        self._user_id = user_id

    def get_genre(self, artist_id):
        url=f"https://api.spotify.com/v1/artists/{artist_id}"
        response=self._place_get_api_request(url)
        response_json = response.json()
        return response_json['genres'][0] if len(response_json['genres'])>0 else 0

        
    def get_last_played_tracks(self, limit=10):
        playedTrackGenres={}
        artist1={}
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        for tracked in response_json['items']:
            artist_id=tracked['track']['artists'][0]['id']
            artist_name=tracked['track']['artists'][0]['name']
            genre=self.get_genre(artist_id)
            playedTrackGenres[genre]=playedTrackGenres.get(genre, 0)+1
            artist1[artist_name]=artist1.get(artist_name, 0)+1

          
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
                  track in response_json["items"]]

        return tracks, playedTrackGenres, artist1

    def get_track_recommendations(self, seed_tracks, limit=50):
        recommendedTrackGenres={}
        artist2={}
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()        
        for tracked in response_json['tracks']:
            artist_id=tracked['album']['artists'][0]['id']
            artist_name=tracked['album']['artists'][0]['name']
            genre=self.get_genre(artist_id)
            recommendedTrackGenres[genre]=recommendedTrackGenres.get(genre, 0)+1
            artist2[artist_name]=artist2.get(artist_name, 0)+1

        print(recommendedTrackGenres)
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]]
        return tracks, recommendedTrackGenres, artist2

    def create_playlist(self, name):
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        print(url)
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return playlist.id
    
    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

