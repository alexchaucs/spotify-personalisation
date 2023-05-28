import tekore as tk
from fastapi import APIRouter, Response, Request
from src.routes.auth import tokens


conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()
router = APIRouter()

@router.get("/")
async def get_playlists(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = tokens.get(userId)
    if token.is_expiring:
        token = cred.refresh(token)
        tokens[userId] = token

    with spotify.token_as(token):
       playlists = spotify.followed_playlists()

    return {"playlists": playlists.items}