import tekore as tk
from typing import Dict
from fastapi import APIRouter, Response, Request
import uuid

conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths: Dict[str, tk.UserAuth] = {}  # User -> Auth object
tokens =  {}   # User -> Access Token object

router = APIRouter()

# Define the scope of your Spotify application
scope = tk.Scope('user-read-currently-playing', 'playlist-modify-private')

@router.get("/login")
async def login(request: Request, response: Response):
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    userId = str(uuid.uuid4())
    response.set_cookie(key="app_spotify_user", value=userId, max_age=604800, httponly=True)
    response.headers["Location"] = auth.url
    response.status_code = 307
    print("User ID set:", userId)
    return {}

@router.get("/callback")
async def callback(request: Request, response: Response, code: str, state: str):
    auth = auths.get(state)  # retrieve the auth associated with this state
    userId = request.cookies.get("app_spotify_user")
    if auth is None:
        return {"error": "Invalid state"}
    try:
        token = auth.request_token(code, state)
        tokens[userId] = token
        return {
            "message": "Authorised successfully",
            "token": token,
            "userId": userId}
    except tk.BadRequest as e:
        return {"error": str(e)}

@router.get("/logout")
async def logout(request: Request, response: Response):
    userId = request.cookies.get("app_spotify_user")

    try:
        if userId in tokens:
            del tokens[userId]  

        if userId in auths:
            del auths[userId]  
        response.delete_cookie("app_spotify_user")
        return {"message": "Logged out successfully"}
    
    except:
        return {"error": "Invalid state"}
