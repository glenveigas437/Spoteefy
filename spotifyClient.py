from track import Track
from playlist import Playlist

class SpotifyClient:
    def get_last_played_tracks(self, response_json):
        playedTrackGenres={}
        artist1={}
        newIds={}
        for tracked in response_json['items']:
            artist_id=tracked['track']['artists'][0]['id']
            artist_name=tracked['track']['artists'][0]['name']
            artist1[artist_name]=artist1.get(artist_name, 0)+1
            newIds[artist_id]=artist_name

          
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
                  track in response_json["items"]]

        return tracks, artist1, newIds
    
    def get_track_recommendations(self, response_json):
        recommendedTrackGenres={}
        artist2={}       
        for tracked in response_json['tracks']:
            artist_id=tracked['album']['artists'][0]['id']
            artist_name=tracked['album']['artists'][0]['name']
            artist2[artist_name]=artist2.get(artist_name, 0)+1

        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]]
        return tracks, artist2
