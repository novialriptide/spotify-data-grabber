# Spotify Data Grabber
Input a Spotify playlist to get a list of the tracks' bpm and key.
<img src="resources/example1.png" width="504" height="400"/>

## Open EXE file
1. Go to your [Spotify](https://developer.spotify.com/dashboard/applications) application dashboard and create an application
2. Go to `src/config.json` and set the proper values for `client_id` and `client_secret`
3. Open the EXE to begin grabbing data

## Build From Source
Follow the steps for **Open EXE file** except for step #3
```
pip install -r requirements.txt
cd src
python main.py
```
