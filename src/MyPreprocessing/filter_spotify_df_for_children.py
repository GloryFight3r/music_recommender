import pandas as pd
import numpy as np
import ast

spotify_df = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/track_features_with_track_id.csv")

spotify_df = spotify_df[spotify_df['danceability'] != -1]

spotify_df['track_ids'] = spotify_df['track_ids'].apply(lambda x: [int(i) for i in ast.literal_eval(x)])

children_songs_only = pd.read_csv("/Users/str1ct0wn3r/Documents/RP/data/Filtered_Data/left_songs.csv")

to_keep = set()

for x in children_songs_only['track_id']:
    to_keep.add(x)

spotify_df = spotify_df[spotify_df['track_ids'].apply(lambda x : bool(set(x) & to_keep))]
spotify_df.reset_index(inplace=True)

print(spotify_df)

spotify_df.to_csv("/Users/str1ct0wn3r/Documents/RP/data/Processed_data/Spotify_Subset/filtered_track_features_for_children.csv", index=False)