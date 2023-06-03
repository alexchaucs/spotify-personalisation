import tekore as tk
from fastapi import APIRouter, Response, Request
from src.services import spotify_service


router = APIRouter()

@router.get("/follow")
async def get_playlists_follow(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = spotify_service.get_token(userId)
    playlists = await spotify_service.get_playlists_follow(token)

    return {"playlists": playlists.items}

