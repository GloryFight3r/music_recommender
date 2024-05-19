import sys

sys.path.insert(0, '/Users/str1ct0wn3r/Documents/RP/src/SpotifyAPI')
sys.path.insert(0, '/Users/str1ct0wn3r/Documents/RP/src')

import spotifyApi
from get_preprocessed_files import load_subsets
import pandas as pd

#token = spotifyApi.authorize()

#print(spotifyApi.get_track_features(token, "7w87IxuO7BDcJ3YUqCyMTT"))

user_index, track_index, u_t_matrix = load_subsets()
spotify_uris = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/raw/spotify-uris.tsv", delimiter="\t")

track_id_to_uri = {}

for x in spotify_uris.to_numpy():
    track_id_to_uri[x[0]] = x[1]


#pd.DataFrame(columns=["track_id", "danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence", "key", "liveness", "loudness", "mode", "speechiness", "time_signature"])

while True:
    df = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features.csv")

    credentials = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/credentials.csv")
    
    if len(credentials) == 0:
            break

    try:
        # read from credentials file
        id = credentials['id'][0]
        secret = credentials['secret'][0]
        credentials = credentials.iloc[1: , :]
        credentials.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/credentials.csv", index=False)
        
        spotifyApi.query_multiple_songs(df, spotify_uris['uri'].to_list(), id, secret)
        df.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features.csv", index=False)
        break
    except Exception as e:
        df.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features.csv", index=False)
        print("here we go again")
"""
try:
    for key, value in track_index.items():
        if value not in all_songs_features:
            df.loc[len(df.index)] = [value, -1, -1, -1, 
                                -1, -1, -1]
            continue

        cur_song_features = all_songs_features[value]

        df.loc[len(df.index)] = [value, cur_song_features["danceability"], cur_song_features["energy"], cur_song_features["instrumentalness"], 
                                cur_song_features["acousticness"], cur_song_features["tempo"], cur_song_features["valence"]]
except Exception as e:
    print(e)
"""