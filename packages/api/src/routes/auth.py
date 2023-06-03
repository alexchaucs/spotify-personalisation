
from fastapi import APIRouter, Request, Response
from src.services import spotify_auth

router = APIRouter()

@router.get("/login")
async def login(request: Request, response: Response):
    auth, userId = spotify_auth.create_auth()
    response.set_cookie(key="app_spotify_user", value=userId, max_age=604800, httponly=True)
    response.headers["Location"] = auth.url
    response.status_code = 307
    return {}

@router.get("/callback")
async def callback(request: Request, response: Response, code: str, state: str):
    userId = request.cookies.get("app_spotify_user")
    auth = spotify_auth.get_auth(userId, state)
    token = spotify_auth.create_token(userId, auth, code, state)
    if token is None:
        response.headers["Location"] = "http://localhost:3000/error"
        response.status_code = 307
        return {}
    else:
        response.headers["Location"] = "http://localhost:3000/success"
        response.status_code = 307
        return {}

@router.get("/logout")
async def logout(request: Request, response: Response):
    userId = request.cookies.get("app_spotify_user")
    success = spotify_auth.logout_user(userId)
    if success:
        response.delete_cookie("app_spotify_user")
        return {"message": "Logged out successfully"}
    else:
        return {"error": "Invalid state"}
