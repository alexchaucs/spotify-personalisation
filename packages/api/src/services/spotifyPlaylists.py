import tekore as tk
import html

class Playlists:
    def __init__(self, token):
        self.spotify = tk.Spotify(token=token, asynchronous=True)

    async def current_user(self):
        return await self.spotify.current_user()

    async def get_playlists_follow(self):
        return await self.spotify.followed_playlists()

    async def _fetch_all_playlists(self, user=None):
        """Fetch all playlists, optionally filtered by a user."""
        playlists = []
        response = await self.spotify.followed_playlists(limit=1)
        total = response.total
        playlists.extend(response.items)
        
        for offset in range(1, total, 10):
            response = await self.spotify.followed_playlists(limit=10, offset=offset)
            playlists.extend(response.items)

        if user:
            playlists = [p for p in playlists if p.owner.uri == user]
        
        return playlists

    async def get_playlists_user(self, user):
        return await self._fetch_all_playlists(user)

    async def get_playlists_data(self, user):
        playlists = await self._fetch_all_playlists(user)
        return [{
            "name": p.name,
            "url": p.images[0].url if p.images else None,
            "description": html.unescape(p.description) if p.description else '',
            "id": p.id
        } for p in playlists]

    async def _fetch_all_playlist_items(self, playlistID):
        """Fetch all items of a playlist."""
        items = []
        response = await self.spotify.playlist_items(playlistID, limit=1)
        total = response.total
        items.extend(response.items)

        for offset in range(1, total, 100):
            response = await self.spotify.playlist_items(playlistID, limit=100, offset=offset)
            items.extend(response.items)

        return items

    async def get_playlist_tracks(self, playlistID):
        return await self._fetch_all_playlist_items(playlistID)

    async def get_playlist_tracks_ids(self, playlistID):
        items = await self._fetch_all_playlist_items(playlistID)
        return [item.track.id for item in items if item.track]

    async def get_tracks_audio_features(self, tracks):
        features = []
        for i in range(0, len(tracks), 50):
            response = await self.spotify.tracks_audio_features(tracks[i:i+50])
            features.extend(response)
        return features

    async def get_playlist_tracks_audio_features(self, playlistID):
        trackIds = await self.get_playlist_tracks_ids(playlistID)
        features = await self.get_tracks_audio_features(trackIds)
        return [feature.__dict__ for feature in features if feature]
