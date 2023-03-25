import tekore as tk
from fastapi import FastAPI, HTTPException, Response, APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

router = APIRouter()

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)


### Environmental Variables
conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()


in_link = '<a href="/login">login</a>'
out_link = '<a href="/logout">logout</a>'
login_msg = f"You can {in_link} or {out_link}"


@router.get("/") # Enforce a html response can use argument response_class=HTMLResponse
def read_root(request: Request):
    user = request.session.get("user", None)
    token = users.get(user, None)

    # Return early if no login or old session
    if user is None or token is None:
        request.session.pop("user", None)
        return HTMLResponse(f"User ID: None<br>{login_msg}")

    page = f"Welcome User ID: {user} <br>{login_msg}"

    # User id for app
    user_id = request.cookies.get("app_spotify_user")
    # response = HTMLResponse()
    cookie_response = {}
    if user_id is None:
        user_id = user
        cookie_response = {"Set-Cookie": f"app_spotify_user={user_id}; Max-Age=604800"}
        # response.headers["Set-Cookie"] = f"app_spotify_user={user_id}; Max-Age=604800"

    page = f"User ID: {user_id}<br>{login_msg}"
    if token.is_expiring:
        token = cred.refresh(token)
        users[user] = token
    try:
        with spotify.token_as(token):
            playback = spotify.playback_currently_playing()
        item = playback.item.name if playback else None
        page += f"<br>Now playing: {item}"
    except tk.HTTPError:
        page += "<br>Error in retrieving now playing!"

    page += f'<br><a href="/playlist">Check out your playlists</a>'
    return HTMLResponse(content = page, headers = cookie_response)

@router.get("/playlist")
def get_playlist(request: Request):
    user = request.session.get("user", None)
    token = users.get(user, None)
    page = "Playlists Image Recommendation"
    # print(user)
    # print(token)
    # if token.is_expiring:
    #     token = cred.refresh(token)
    #     users[user] = token
    try:
        with spotify.token_as(token):
            playback = spotify.followed_playlists()
        # for playlist in playback.items:
        #     i

        for i, item  in enumerate(playback.items):
            name =item.name
            url = item.images[0].url
            width = item.images[0].width
            height = item.images[0].height

            page += f"<br>Name: {name}"
            page += f"<br><html><body><p><img src = '{url}' style='width:{150}px;height:{150}px;'></a</p><html><body>"
            if i == 1:
                break
    except tk.HTTPError:
        page += "<br>Error in retrieving now playing!"
    return HTMLResponse(content = page)


@router.get("/login")
def login(request: Request):
    if "user" in request.session:
        return RedirectResponse(url="/")

    scope = tk.Scope('user-read-currently-playing', 'playlist-modify-private')
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    return RedirectResponse(auth.url)


@router.get("/callback")
def login_callback(request: Request, code: str, state: str):
    auth = auths.pop(state, None)

    if auth is None:
        return "Invalid state!", 400

    token = auth.request_token(code, state)
    request.session["user"] = state
    users[state] = token
    return RedirectResponse("/")


@router.get("/logout")
def logout(request: Request):
    uid = request.session.pop("user", None)
    if uid is not None:
        users.pop(uid, None)
    return RedirectResponse("/")