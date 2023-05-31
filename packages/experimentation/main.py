import asyncio
import tekore as tk

from collections import Counter

# conf = tk.config_from_environment()
# scope = tk.scope.playlist_read_private
# token = tk.prompt_for_user_token(*conf, scope=scope)

conf = tk.config_from_environment()
token = tk.prompt_for_user_token(*conf)
spotify = tk.Spotify(token)

spotify.current_user()
current_user = spotify.current_user().uri

for i, playlist in enumerate(spotify.playlists('gingerale3').items):
    if playlist.owner.uri != spotify.current_user().uri:
        continue
    print(f"Idx {i}, name: {playlist.name}", )
    for j in playlist.images:
        print(f"height: {j.height}, width: {j.width}, url: {j.url}")

    print("---------------------------")


    


playlist = spotify.followed_playlists(limit=1).items[0]
track = spotify.playlist_items(playlist.id, limit=1).items[0].track
name = f'"{track.name}" from {playlist.name}'

if track.episode:
    print(f'Cannot analyse episodes!\nGot {name}.')
elif track.track and track.is_local:
    print(f'Cannot analyse local tracks!\nGot {name}.')
else:
    print(f'Analysing {name}...\n')
    analysis = spotify.track_audio_features(track.id)
    print(repr(analysis))

    

def get_artist(track) -> str:
    if track.episode:
        return track.show.name
    else:
        return track.artists[0].name

async def count_artists(spotify: tk.Spotify, playlist_id: str):
    tracks = await spotify.playlist_items(playlist_id)
    tracks = spotify.all_items(tracks)
    return Counter([get_artist(t.track) async for t in tracks])


async def main() -> Counter:
    sender = tk.RetryingSender(sender=tk.AsyncSender())
    spotify = tk.Spotify(token, sender=sender, max_limits_on=True)

    playlists = await spotify.followed_playlists()
    playlists = spotify.all_items(playlists)
    counts = [await count_artists(spotify, p.id) async for p in playlists]

    await spotify.close()
    return sum(counts, Counter())


artists = asyncio.run(main())

for name, count in artists.most_common(3):
    print(count, name)