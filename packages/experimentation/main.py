import asyncio
import tekore as tk

from collections import Counter

conf = tk.config_from_environment()
scope = tk.scope.playlist_read_private
token = tk.prompt_for_user_token(*conf, scope=scope)


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