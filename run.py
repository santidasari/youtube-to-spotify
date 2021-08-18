import os


from youtube_client import YoutubeClient
from spotify_client import SpotifyClient


def run():
    #getting our playlist from youtube
    youtube_client = YoutubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_TOKEN'))
    playlists= youtube_client.get_playlists()

    #getting the playlist we want to get music from
    for index,playlist in enumerate(playlists):
        print("{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print("You selected: {chosen_playlist.title}")
   
   
    #get song info from youtube for the videos in our selected playlist
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print("Attempting to add {len(songs)}")
   
   
    #search if the song is on spotify
    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
    #if song is found, add it to spotify liked songs/ playlist
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print("Added {song.artist}")







if __name__== '__main__':
    run()