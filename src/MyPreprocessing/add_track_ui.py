import pandas as pd
import numpy as np

spotify_uris = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/raw/spotify-uris.tsv", delimiter="\t")

track_uri = dict()
for x in spotify_uris.to_numpy():
    if x[1] not in track_uri:
        track_uri[x[1]] = list()
    track_uri[x[1]].append(x[0])

spotify_feat = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features.csv")

dd = []
for x in spotify_feat.to_numpy():
    dd.append([track_uri[x[0]], x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]])

df = pd.DataFrame(data=dd, columns=['track_ids','spotify_uri','danceability','energy','instrumentalness','acousticness',
                           'tempo','valence','key','liveness','loudness',
                           'mode','speechiness','time_signature'])
df.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features_with_track_id.csv", index=False)