import tekore as tk
from fastapi import APIRouter, Response, Request
from src.services import spotify_auth
from src.services.spotifyPlaylists import Playlists


router = APIRouter()

@router.get("/follow")
async def get_playlists_follow(request: Request):
    playlist_user = Playlists()
    userId = request.cookies.get("app_spotify_user")
    token = spotify_auth.get_token(userId)
    await playlist_user.get_playlists_follow(token)

    return {"playlists": playlist_user.followed_playlists.items}

