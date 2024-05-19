import requests
import base64
import json
import math
import time
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

#CLIENT_ID = "d10ee1d60570431e923d4ee584137381"
#CLIENT_SECRET = "f70b4abde38147c9a24c4839b9d857cc"

TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/authorize"
REDIRECT_URI = "http://localhost:8888/callback"

def authorize(CLIENT_ID, CLIENT_SECRET):
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    res = requests.post(TOKEN_URL, headers=headers,data=data)

    json_result = json.loads(res.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token
    }

def get_all_track_audio_features(token, id):
    headers = get_auth_header(token)
    url = "https://api.spotify.com/v1/audio-features/" + id

    res = requests.get(url, headers=headers)

    #print(res.headers.get('Retry-After'), "DAS")

    json_result = json.loads(res.content)

    return json_result

def get_track(token, id):
    headers = get_auth_header(token)
    url = "https://api.spotify.com/v1/tracks/" + id

    res = requests.get(url, headers=headers)
    json_result = json.loads(res.content)

    return json_result

def get_track_features(token, id):
    track_features = get_all_track_audio_features(token, id)

    if 'error' in track_features:
        return {"error":"-1"}

    wanted_features = ["danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence"]

    result = {}

    for wanted_feature in wanted_features:
        result[wanted_feature] = track_features[wanted_feature]

    return result

def get_multiple_tracks(token, id):
    headers = get_auth_header(token)

    while True:
        try:
            url = "https://api.spotify.com/v1/audio-features?" + "ids=" + id

            res = requests.get(url, headers=headers)

            json_result = json.loads(res.content)

            return json_result
        except Exception as e:
            print(e)   

def get_multiple_track_features(token, df:pd.DataFrame, ids, all_ids):
    track_features = get_multiple_tracks(token, ids)

    wanted_features = ["danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence"]

    vis = set()

    for x in track_features['audio_features']:
        if x == None:
            continue
        vis.add(x['id'])
        df.loc[len(df.index)] = [x['id'], x["danceability"], x["energy"], x["instrumentalness"], 
                                x["acousticness"], x["tempo"], x["valence"], x["key"], x["liveness"],
                                x["loudness"], x["mode"], x["speechiness"], x["time_signature"]]

    for x in all_ids:
        if x not in vis:
            df.loc[len(df.index)] = [x, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

def request_multiple_features(sp: spotipy.Spotify, ids):
    track_features = sp.audio_features(ids)

    wanted_features = ["danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence"]

    result = {}

    for x in track_features:
        if x == None:
            continue
        result[x['id']] = {}
        for wanted_feature in wanted_features:
            result[x['id']][wanted_feature] = x[wanted_feature]

    for x in ids:
        if x not in result:
            result[x] = {}
            for wanted_feature in wanted_features:
                result[x][wanted_feature] = "-1"

    return result

def query_multiple_songs(df:pd.DataFrame, ids:list[str], CLIENT_ID, CLIENT_SECRET):
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))
    token = authorize(CLIENT_ID, CLIENT_SECRET)

    cur_contained = set()

    for x in df['track_id']:
        cur_contained.add(x)
    
    new_ids = []
    for x in ids:
        if x not in cur_contained:
            new_ids.append(x)
    np_ids = np.array(new_ids)

    print(len(np_ids))

    BATCH_SIZE = 100
    K = math.ceil(len(np_ids) / BATCH_SIZE)
    PER_WINDOW = 50
    HARD_RESET_PER_WINDOW = 1500
    #print("AS")
    for i in range(K):
        query = ','.join(np_ids[i*BATCH_SIZE:(i+1)*BATCH_SIZE])
        get_multiple_track_features(token, df, query, np_ids[i*BATCH_SIZE:(i+1)*BATCH_SIZE])

        if i > 0 and i % PER_WINDOW == 0:
            print("Processed", (i * BATCH_SIZE)/len(np_ids)*100, "of the data!")
            #break
            time.sleep(0.4)
    

#print(get_multiple_tracks(authorize(), "5Dp0mpWGUFAto3TzHdrp0x"))
#print(query_multiple_songs(pd.DataFrame(columns=["track_id", "danceability", "energy", "instrumentalness", "acousticness", "tempo", "valence"]), ["5Dp0mpWGUFAto3TzHdrp0x"]))