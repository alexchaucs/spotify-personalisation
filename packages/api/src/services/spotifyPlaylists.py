import tekore as tk
from typing import Dict
import uuid
import asyncio
import html

class Playlists:
    def __init__(self, token):
        self.spotify = tk.Spotify(token = token, asynchronous=True)

    async def current_user(self):
        return await self.spotify.current_user()


    async def get_playlists_follow(self):
        return await self.spotify.followed_playlists() #followed_playlists

    async def get_playlists_user(self, user):
        playlists = []
        inital_response = await self.spotify.followed_playlists(limit = 1, offset = 0)
        total = inital_response.total 
        playlists.extend(inital_response.items)
        limit = 10
        numOfCalls = (total - 1)//limit + 1
        
        tasks = [self.spotify.followed_playlists(limit = limit, offset = 1 + limit * i) for i in range(numOfCalls)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            playlists.extend(response.items)

        userPlaylists = []
        for i, playlist in enumerate(playlists):
            if playlist.owner.uri != user:
                continue
            userPlaylists.append(playlist)

        return userPlaylists


    async def get_playlists_data(self, user):
        playlists = []
        inital_response = await self.spotify.followed_playlists(limit = 1, offset = 0)
        total = inital_response.total 
        playlists.extend(inital_response.items)
        limit = 10
        numOfCalls = (total - 1)//limit + 1
        
        tasks = [self.spotify.followed_playlists(limit = limit, offset = 1 + limit * i) for i in range(numOfCalls)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            playlists.extend(response.items)

        userPlaylistsData = []
        for i, playlist in enumerate(playlists):
            if playlist.owner.uri != user:
                continue
            userPlaylistsData.append({
                "name": playlist.name,
                "url": playlist.images[0].url,
                "description": html.unescape(playlist.description),
                "id": playlist.id
                })

        return userPlaylistsData

    async def get_playlist_tracks(self, playlistID: str):
        playlistData = []
        inital_response = await self.spotify.playlist_items(playlistID, limit = 1, offset = 0)
        total = inital_response.total 
        playlistData.extend(inital_response.items)
        limit = 100
        numOfCalls = (total - 1)//limit + 1
        
        tasks = [self.spotify.playlist_items(playlistID, limit = limit, offset = 1 + limit * i) for i in range(numOfCalls)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            playlistData.extend(response.items)

        return playlistData