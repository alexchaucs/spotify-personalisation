import tekore as tk
from fastapi import APIRouter, Response, Request
from src.services import spotify_service


router = APIRouter()

@router.get("/get_playlists")
async def get_playlists(request: Request):
    userId = request.cookies.get("app_spotify_user")
    token = spotify_service.get_token(userId)
    playlists = spotify_service.get_playlists(token)

    return {"playlists": playlists.items}

