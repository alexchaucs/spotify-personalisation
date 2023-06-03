import tekore as tk
from fastapi import APIRouter, Response, Request
from src.services import spotify_auth
from src.services.spotifyPlaylists import Playlists


router = APIRouter()

@router.get("/me")
async def get_uri(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = spotify_auth.get_token(userId)
    playlist = Playlists(token)
    playlist.current_user_uri = await playlist.current_user()
    return {"current_user_uri": playlist.current_user_uri}

@router.get("/follow")
async def get_playlists_follow(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = spotify_auth.get_token(userId)
    playlist = Playlists(token)
    playlist.followed_playlists = await playlist.get_playlists_follow()
    print(len(playlist.followed_playlists.items))
    return {"followed_playlists": playlist.followed_playlists.items}


@router.get("/user")
async def get_playlists_user(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = spotify_auth.get_token(userId)
    playlist = Playlists(token)
    current_user_uri = await playlist.current_user()
    playlist.user_playlists = await playlist.get_playlists_user(current_user_uri.uri)
    print(len(playlist.user_playlists))
    return {"user_playlists": playlist.user_playlists}


