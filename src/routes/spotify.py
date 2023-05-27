import tekore as tk
from typing import Dict
from fastapi import APIRouter, responses
'''
Sample process

1.
http://localhost:5000/login

Initial login request
* Generates a auth object
    - has redirect url
    - has state

Hold auths[state] = auth * so we know which auth object were are using given a state


2. Once authorise on redirect link
This validates the auth object

By equating the states, you can find the authenticated auth object

Use validated auth object to generate access token


3. Perform a request on playlist route
Only needs an access token
Create a Spotify client object with the user's access token
Requests data
    

'''

conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths: Dict[str, tk.UserAuth] = {}  # we'll use this to store ongoing authorisations
users = {}  # User tokens: state -> token (use state as a user ID)
tokens = {}
router = APIRouter()

# Define the scope of your Spotify application
scope = tk.Scope('user-read-currently-playing', 'playlist-modify-private')

@router.get("/login")
async def login():
    # Create new UserAuth object
    auth = tk.UserAuth(cred, scope)

    # State value generated during initial auth request
    auths[auth.state] = auth  # add the new authorisation to our dict
    # Returns link to redirect the user to the Spotify authorisation page
    return {
        "url": auth.url,
        "state": auth.state
        } 

# Once authorised - spotify redirects to callback route
# Receives a get request at this route with code and state as query parameters
@router.get("/callback")
async def callback(code: str, state: str):
    # return {
    #     "code": code,
    #     "state": state
    # }
    auth = auths.get(state)  # retrieve the auth associated with this state
    if auth is None:
        return {"error": "Invalid state"}
    try:
        # exchange the code for tokens and store them in the auth instance
        # checks that state from initial request matches the redirected state
        token = auth.request_token(code, state)
        tokens['test'] = token
        # return responses.RedirectResponse("/playlists?state='a'")
        return {
            "message": "Authorised successfully",
            "token": token}
    except tk.BadRequest as e:
        return {"error": str(e)}

@router.get("/playlists")
async def get_playlists(state: str): #state can be optional
    # auth = auths.get(state)  # retrieve the auth associated with this state

    # if auth is None:
    #     return {"error": "Invalid state"}

    # refresh the access token if it's expiring
    # Only needs access token to pull data
    token = tokens['test']

    if token.is_expiring:
        token = cred.refresh(token)
        tokens['test'] = token

    # Create a Spotify client with the user's access token
    with spotify.token_as(token):
       ## Get the user's playlists
       playlists = spotify.followed_playlists()

    return {"playlists": playlists.items}

@router.get("/logout")
async def logout(state: str):
    if state in auths:
        del auths[state]  # remove the auth associated with this state
        return {"message": "Logged out successfully"}
    else:
        return {"error": "Invalid state"}
