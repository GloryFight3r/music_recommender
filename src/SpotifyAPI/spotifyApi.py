import requests
import base64
import json

CLIENT_ID = "439d33487a8e4145a5e1bad310a32836"
CLIENT_SECRET = "bfe8d64e7b264a73af6f867d860a3985"

TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/authorize"

def authorize():
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
    return {"Authorization": "Bearer " + token}

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

token = authorize()
print(get_all_track_audio_features(token, "7w87IxuO7BDcJ3YUqCyMTT"))
