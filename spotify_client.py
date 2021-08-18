import requests
import urllib.parse



class SpotifyClient(object):
    def __init__(self):
        self.api_token = api_token

    def search_song(self,artist,song):
        query = urllib.parse.quote(f'{artist} {song}')
        url = "https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {self.api_token}"
            }
        )
        response_json = response.json()

        results = response_json['tracks']['items']

        if results:
            return results[0]['id']
        else:
            raise Exception("No song found for {artist} = {song}")

    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"

        response = requests.put(
            url,
            json={
                "ids" :[song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {self.api_token}"
            }
        )

        return response.ok
