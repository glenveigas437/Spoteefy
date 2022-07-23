import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import json
import time
import pandas as pd
from credentials import *
from SpotifyClient import *
import pygal

# App config
app = Flask(__name__)

app.secret_key = #YOUR SECRET KEY

spotifyClient = SpotifyClient()

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("home")



@app.route('/logout')
def logout():
	for key in list(session.keys()):
		session.pop(key)
	return redirect('/')


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read playlist-modify-public")

def getStatus():
	session['token_info'], authorized = get_token()
	session.modified = True
	if not authorized:
		return redirect('/')
	sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
	return sp

@app.route('/home')
def home():
	sp=getStatus()
	return render_template("home.html", userName=sp.current_user()['display_name'])

@app.route('/getVisualize', methods=['POST'])
def getVisualize():
	sp =getStatus()

	trackInput=request.form['trackInput']
	trackInput=int(trackInput)
	
	global lastPlayedTracks
	global artist
	global artistIds
	
	curGroup = sp.current_user_saved_tracks(limit={trackInput})
	lastPlayedTracks,artist,artistIds = SpotifyClient().get_last_played_tracks(curGroup)
	trackIndex, trackName = [], []

	for tracks in range(len(lastPlayedTracks)):
		trackIndex.append(tracks+1)
		trackName.append(lastPlayedTracks[tracks])

	tempDF={
	'Track': trackIndex,
	'Name': trackName
	}

	playedTracksDF=pd.DataFrame(tempDF, columns=['Track', 'Name'])

	return render_template('visualizeTracks.html', playedTracksDF=playedTracksDF.to_dict(orient='records'))

def calc(num, den):
	return round((num/den)*100, 2)

@app.route('/visualizeGenresArtists')
def visualize():
	sp=getStatus()

	artists = list(artist.keys())
	frequency = list(artist.values())
	artistIdsList = list(artistIds.keys())
	genres = {}

	for i in artistIdsList:
		genre=sp.artist(i)['genres'][0]
		genres[genre]=genres.get(genre, 0)+1

	
	tempDF={'Artist': artists, 'Frequency': frequency}

	artistDF = pd.DataFrame(tempDF, columns=['Artist', 'Frequency'])

	pie_chart = pygal.Pie(inner_radius=.4)
	pie_chart.title = 'Genre Distrbution(%) of the tracks you Love'
	for i in genres:
		pie_chart.add(i, calc(genres[i], sum(genres.values())))
	
	
	pie_chart = pie_chart.render_data_uri()

	return render_template('visualizeGenreArtist.html', artistDF=artistDF.to_dict(orient='records'), pie_chart=pie_chart)

@app.route('/getRecommend', methods=['POST'])
def getRecommend():
	sp=getStatus()
	trackNumInput=request.form['trackNumInput']
	indexes = trackNumInput.split()
	seed_tracks = [lastPlayedTracks[int(index)-1].id for index in indexes]
	
	global recommendedTracks
	global artistNew

	recommendedTracks,artistNew=SpotifyClient().get_track_recommendations(sp.recommendations(seed_tracks=seed_tracks))
	
	trackIndex=[]
	trackName=[]
	for tracks in range(len(recommendedTracks)):
		trackIndex.append(tracks+1)
		trackName.append(recommendedTracks[tracks])

	tempDF={
	'Track': trackIndex,
	'Name': trackName
	}

	recommendedTracksDF=pd.DataFrame(tempDF, columns=['Track', 'Name'])

	return render_template('recommendedTracks.html', recommendedTracksDF=recommendedTracksDF.to_dict(orient='records'))

@app.route('/createPlaylist', methods=['POST'])
def createPlaylist():
	sp=getStatus()
	id=sp.current_user()['id']
	playlistName = request.form['playlistName']
	playlist = sp.user_playlist_create(user=id, name=playlistName, public=True)
	playlistId=playlist['id']
	recPlay = [recommendTrack.id for recommendTrack in recommendedTracks]
	sp.playlist_add_items(playlist_id=playlist['id'], items=recPlay)
	
	return render_template('successPage.html', playlistName=playlistName, playlistId=playlistId)



if __name__ == '__main__':
	app.run(debug=True)
