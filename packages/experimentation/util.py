import asyncio
import tekore as tk

async def fetch_playlists(spotify: tk.Spotify, userID: str):
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
    

async def get_playlist_tracks_ids(spotify, playlistID: str):
    playlistTracks = []
    inital_response = await spotify.playlist_items(playlistID, limit = 1, offset = 0)
    total = inital_response.total 
    playlistTracks.extend(inital_response.items)
    limit = 50
    numOfCalls = (total - 1)//limit + 1
    
    tasks = [spotify.playlist_items(playlistID, limit = limit, offset = 1 + limit * i) for i in range(numOfCalls)]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        playlistTracks.extend(response.items)

    return playlistTracks#[track.track.id for track in playlistTracks]


async def get_tracks_audio_features(spotify, tracks: list):
    trackFeatures = []
    total = len(tracks)
    limit = 50
    numOfCalls = (total)//limit + 1
    
    tasks = [spotify.tracks_audio_features(tracks[i*limit : (i + 1) * limit]) for i in range(numOfCalls)]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        if response is not None:
            trackFeatures.extend(response)

    return trackFeatures


async def get_playlists_audio_features(spotify, playlists_ids: list):

    tasks = [get_playlist_tracks_ids(spotify, id) for id in playlists_ids]
    
    return [track.__dict__ for track in trackFeatures if track is not None]
