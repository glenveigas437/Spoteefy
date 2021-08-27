# Spoteefy

Spoteefy is a Python web app built using Flask that leverages the power of Spotify's web API and recommends a new playlist to the user based on the user's playback history.

## Why The Name 'Spoteefy'?
In search of creative names, Spoteefy is a portmanteau for 'Spotify' - The Music streaming app and 'Seed' for Seed based approach.

## Motivation
Spotify creates a playlist for it's users every week named 'Discover Weekly' based on the playback history of the user. Now this has not been received well by few users, while some are just so content with what Spotify recommends to the user. So to tackle the lack of contentment among the former set of users this web app lets the user decide what he/she would like to listen based on the selection of their desired tracks. 

## Prequisites
1) Spotify Account
2) Spotify Developer's Account.
And we good to go.

## Spotify Web API and it's use in Spoteefy Web App
You can read more about [Spotify's Web API](https://developer.spotify.com/) here and play with it's functionalities. To build this web app all you need is i) OAuth Token ii) User ID. 

## Functionalities 
1) Get User's last 'N' Played tracks N can range from (1-50)
2) Recommend the user new tracks based on what tracks the user selects.
3) Create a new Playlist.
4) Get Statistics on user's taste of music.

## Let's dive deep into this

### Getting the OAuth Token and User ID from the Developer's site.
head over to https://developer.spotify.com/console/get-current-user/

(![Developer Console to get Current User details](https://user-images.githubusercontent.com/31877827/131079837-851f2bb3-b17a-46c6-ae26-d1b051215b04.png)

Click on Try it and you get all the details in a json format on the right corner, you can copy the user id from right there.

![image](https://user-images.githubusercontent.com/31877827/131080277-01376c1b-90ff-4808-bb8e-8e349b000758.png)

Next head over to the Playlist section and click on Create a Playlist https://developer.spotify.com/console/post-playlists/

Click on Get Token and select these options

![image](https://user-images.githubusercontent.com/31877827/131080555-41135b50-a0c8-493b-a426-6c0a6cabc278.png)

and request the token. This Web app contains a [YAML file](https://github.com/glenveigas437/Spoteefy/blob/main/auth.yaml), where the userID and oAuth token is added.

### Running the app
You can clone or download the repo.
1) Install all dependencies in ```requirements.txt``` file
2) Go inside your Terminal or Command Prompt and type ```python3 app.py``` or ```python app.py``` respectively
3) Open the link

### Home Page

![Home Page](https://user-images.githubusercontent.com/31877827/131081225-6cfcaf56-877c-438a-ad68-1cd53346b301.png)

Enter the number of tracks you want to visualize, for this instance I selected 10

### Tracks based on Playback History

![image](https://user-images.githubusercontent.com/31877827/131081975-2f0b9c82-b437-4624-96cb-b39913982adc.png)

### Stats based on your Favourite Artists

![image](https://user-images.githubusercontent.com/31877827/131082099-1a82db31-5c03-4301-8e25-a0b1120429e2.png)

### Genre Stats

![image](https://user-images.githubusercontent.com/31877827/131082185-5ec176b5-0c9d-4c7f-a748-5879dccea6e9.png)

I have now selected tracks 1,4,7,8,9 to create my desired playlist
based on the details of these tracks like artist, genre, audio features I get a new playlist

### New Recommended Tracks
The user gets a list of 50 Tracks, the user can visualize about the Genre and artist too.

![image](https://user-images.githubusercontent.com/31877827/131082482-816f1f7b-ecc9-437d-bf1a-e06bbb54c59e.png)
 
### Creating a New Playlist

![image](https://user-images.githubusercontent.com/31877827/131082663-29d6cfb6-7dd8-47b1-9890-3e42fa0e3d5d.png)

Give any name you want.

### Confirmation Page

![image](https://user-images.githubusercontent.com/31877827/131082786-c33e6916-795f-41ef-91c8-1a2fe2f65b41.png)

You can now click on that button and view your new playlist.

### The Playlist in Spotify

![image](https://user-images.githubusercontent.com/31877827/131082945-ae131407-3ae2-465e-9296-e9a8e4519e5e.png)

