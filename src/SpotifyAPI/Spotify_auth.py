import spotipy
from flask import Flask, request, render_template, redirect, session, url_for
from flask_session import Session
import time
import requests
import os
import random

# Create app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['SESSION_COOKIE_SECURE'] = True

# get environment variables
dotenv_path = "credentials.env"


redirect_uri = "http://127.0.0.1:5000/callback"
token_url = "https://accounts.spotify.com/api/token"
auth_url = "https://accounts.spotify.com/authorize"
client_id = "439d33487a8e4145a5e1bad310a32836"
client_secret = "bfe8d64e7b264a73af6f867d860a3985"
scope = os.getenv("scope") # user-read-private user-read-email user-read-recently-played user-top-read playlist-modify-private playlist-modify-public

sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                      redirect_uri=redirect_uri)


# Starting point of the application
@app.route('/')
def index():
    # Generate a random ID for the user
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print(user_id)
    # Store the user ID in the session
    session['user_id'] = user_id
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# callback route, after Spotify login, redirects to loading screen
@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Make a request to the Spotify API to get the access token
    resp = requests.post(token_url,
                            auth=HTTPBasicAuth(client_id, client_secret),
                            data={
                                'grant_type': 'authorization_code',
                                'code': code,
                                'redirect_uri': redirect_uri
                            })
    refresh_token = resp.json()['refresh_token']
    access_token = resp.json()['access_token']
    expires_in = resp.json()['expires_in']

    if access_token:
        
        # Get the refresh token
        expiration_time = time.time() + expires_in
        session['refresh_token'] = refresh_token
        session['expiration_time'] = expiration_time
        
        # Store the access token in the session
        session['access_token'] = access_token
        user_id = session.get('user_id')

    sp = spotipy.Spotify(auth=access_token)
    
    
    #Now you can use the Spotify API with the access token
    
    
    # Do some computations here, after a while ask for the access token again
    # It should be valid for an hour, but if there are a lot of requests, do it to be sure
    ###########################################################
    
    
    
    access_token = session.get('access_token')
        
    # Get refresh token and expiration time from the session
    expiration_time = session.get('expiration_time')
    current_time = time.time()
    
    # Check if the access token is still valid
    if current_time < expiration_time:
        print("Access token is valid")
    else:
        print("Access token has expired")
        #refresh the token
        refresh_token = session.get('refresh_token')
        token_info = sp_oauth.refresh_access_token(refresh_token) 
        
        access_token = token_info['access_token']
        
    # Create a new Spotipy client with the access token
    sp = spotipy.Spotify(auth=access_token)