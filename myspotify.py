import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="c1ebf6c270e7494190ade10285721a01",
                                                           client_secret="878c4ab18b6346d384ce312224aa98c6"))
