import sys

sys.path.insert(0, '/Users/str1ct0wn3r/Documents/RP/src/SpotifyAPI')
sys.path.insert(0, '/Users/str1ct0wn3r/Documents/RP/src')

import spotifyApi
from get_preprocessed_files import load_subsets
import pandas as pd

token = spotifyApi.authorize()

#print(spotifyApi.get_track_features(token, "7w87IxuO7BDcJ3YUqCyMTT"))

user_index, track_index, u_t_matrix = load_subsets()
spotify_uris = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/raw/spotify-uris.tsv", delimiter="\t")

track_id_to_uri = {}

for x in spotify_uris.to_numpy():
    track_id_to_uri[x[0]] = x[1]

#print(spotify_uris)

df = pd.DataFrame(columns=["track_id", "danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence"])

for key, value in track_index.items():
    #print(track_id_to_uri[value])
    track_features = spotifyApi.get_track_features(token, track_id_to_uri[value])
    if "error" in track_features:
        df.loc[len(df.index)] = [value, -1, -1, -1, -1, -1, -1]
    else:
        df.loc[len(df.index)] = [value, track_features["danceability"], track_features["energy"], track_features["instrumentalness"], 
                             track_features["acousticness"], track_features["tempo"], track_features["valence"]]
    
df.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Spotify_Subset/track_features.csv", index=True)