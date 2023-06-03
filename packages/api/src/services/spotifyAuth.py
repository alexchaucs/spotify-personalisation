import tekore as tk
from typing import Dict
import uuid

class SpotifyAuth:
    def __init__(self):
        self.conf = tk.config_from_environment()
        self.cred = tk.Credentials(*self.conf)
        self.spotify = tk.Spotify(asynchronous=True)
        self.auths: Dict[str, tk.UserAuth] = {}  # User -> state -> Auth object
        self.tokens =  {}   # User -> Access Token object
        self.scope = tk.Scope('user-read-currently-playing', 'playlist-modify-private')

    def create_auth(self):
        auth = tk.UserAuth(self.cred, self.scope)
        userId = str(uuid.uuid4())
        self.auths[userId] = {auth.state: auth}
        return auth, userId

    def get_auth(self, userId: str, state: str):
        return self.auths.get(userId).get(state)

    def delete_auth(self, state: str):
        if state in self.auths:
            del self.auths[state]

    def create_token(self, userId: str, auth: tk.UserAuth, code: str, state: str):
        token = auth.request_token(code, state)
        self.tokens[userId] = token
        return token

    def get_token(self, userId: str):
        token = self.tokens.get(userId)
        if token.is_expiring:
            token = self.cred.refresh(token)
            self.tokens[userId] = token
        return token
    
    def delete_token(self, state: str):
        if state in self.tokens:
            del self.tokens[state]
    
    def logout_user(self, userId):
        try:
            if userId in self.tokens:
                del self.tokens[userId]  
            if userId in self.auths:
                del self.auths[userId]  
            return True
        
        except:
            return False

    async def fetch_playlists(self, spotify: tk.Spotify, userID: str):
        playlists = []
        inital_response = await spotify.playlists(userID, limit = 1, offset = 0)
        total = inital_response.total 
        playlists.extend(inital_response.items)
        limit = 10
        numOfCalls = (total - 1)//limit + 1
        
        tasks = [spotify.playlists(user_id=userID, limit = limit, offset = 1 + limit * i) for i in range(numOfCalls)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            playlists.extend(response.items)

        return playlists

    async def get_playlists_follow(self, token):
        with self.spotify.token_as(token):
            return await self.spotify.followed_playlists()