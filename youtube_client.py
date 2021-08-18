import os

import google_auth_oauthlib
import googleapiclient.discovery
import youtube_dl



class Playlist(object):
    def __init__(self,id,title):
        self.id = id
        self.title = title

class Song(object):
    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

class YoutubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

    # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client



    def get_playlists(self):
        request = self.youtube_client.playlists().list(part="id, snippet", maxResults=25, mine=True)
        response = request.execute()

        #go through responses disctionary and get items which will grab playlist as a list
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists

    def get_videos_from_playlist(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(playlistId=playlist_id, part="id, snippet")

        response = request.execute()

       
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist, song = self.get_artist_and_song(video_id)
            if artist and song:
                songs.append(Song(artist, song))
        return songs


    def get_artist_and_song(self, video_id):
        youtube_url = "https://www.youtube.com/watch?v={video_id}"
         #using youtube dl library
        video = youtube_dl.YoutubeDL({'quiet':True}).extract_info(youtube_url, download=False) 

        artist = video['artist']
        song = video['track']

        return artist,song

