import tekore as tk
from typing import Dict
import uuid

class Playlists:
    def __init__(self):
        self.spotify = tk.Spotify(asynchronous=True)

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
            self.followed_playlists = await self.spotify.followed_playlists()
            return 