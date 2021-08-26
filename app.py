from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
from spotifyClient import *
from track import *
from playlist import *
import yaml
import pygal



app = Flask(__name__)


with open('auth.yaml') as auth:
    
    data = yaml.load(auth, Loader=yaml.FullLoader)

userAuthToken=data['authToken']
userID=data['userID']

spotify_client = SpotifyClient(userAuthToken, userID)

@app.route('/')
def root():

	return render_template('home.html')


@app.route('/getVisualize', methods=['POST'])
def getVisualize():
	trackInput=request.form['trackInput']
	trackInput=int(trackInput)
	
	global lastPlayedTracks
	global playedTrackGenres
	global artist
	
	lastPlayedTracks, playedTrackGenres, artist = spotify_client.get_last_played_tracks(trackInput)
	trackIndex=[]
	trackName=[]
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
	artists = list(artist.keys())
	frequency = list(artist.values())

	tempDF={'Artist': artists, 'Frequency': frequency}

	artistDF = pd.DataFrame(tempDF, columns=['Artist', 'Frequency'])

	pie_chart = pygal.Pie(inner_radius=.4)
	pie_chart.title = 'Genre Distrbution(%) of the tracks you Love'
	for i in playedTrackGenres:
		pie_chart.add(i, calc(playedTrackGenres[i], sum(playedTrackGenres.values())))
	
	pie_chart = pie_chart.render_data_uri()

	return render_template('visualizeGenreArtist.html', artistDF=artistDF.to_dict(orient='records'), pie_chart=pie_chart)


@app.route('/getRecommend', methods=['POST'])
def getRecommend():
	trackNumInput=request.form['trackNumInput']
	indexes = trackNumInput.split()
	seed_tracks = [lastPlayedTracks[int(index)-1] for index in indexes]
	
	global recommendedTracks
	global recommendedTrackGenres
	global artistNew

	recommendedTracks, recommendedTrackGenres, artistNew = spotify_client.get_track_recommendations(seed_tracks)
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

@app.route('/recommendGenresArtists')
def recommend():
	artists = list(artistNew.keys())
	frequency = list(artistNew.values())

	tempDF={'Artist': artists, 'Frequency': frequency}

	artistDF = pd.DataFrame(tempDF, columns=['Artist', 'Frequency'])

	pie_chart = pygal.Pie(inner_radius=.4)
	pie_chart.title = 'Genre Distrbution(%) of the tracks you Love'
	for i in recommendedTrackGenres:
		pie_chart.add(i, calc(recommendedTrackGenres[i], sum(recommendedTrackGenres.values())))
	
	pie_chart = pie_chart.render_data_uri()

	return render_template('visualizeGenreArtist.html', artistDF=artistDF.to_dict(orient='records'), pie_chart=pie_chart)

@app.route('/createPlaylist', methods=['POST'])
def createPlaylist():
	playlistName = request.form['playlistName']
	playlist = spotify_client.create_playlist(playlistName)
	global playlistID
	playlistID=spotify_client.populate_playlist(playlist, recommendedTracks)
	
	return render_template('successPage.html', playlistID=playlistID, playlistName=playlistName)



app.run(debug=True)

