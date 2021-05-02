from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"

date = input("Which year do you want to travel to?"
             " Type the date in this format YYYY-MM-DD: ")


bill_board_url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=bill_board_url)
bill_board_web = response.text

soup = BeautifulSoup(bill_board_web, "html.parser")

all_songs_tags = soup.find_all(name="span", class_="chart-element__information__song")

songs_title = [tags.getText() for tags in all_songs_tags]

spotipy_oath = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = spotipy_oath.current_user()["id"]
song_uris = []

for song in songs_title:
    result = spotipy_oath.search(
        q=f"track:{song} year:{date.split('-')[0]}",
        type="track"
    )
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in the spotify")
        pass
create_playlist = spotipy_oath.user_playlist_create(name=f"{date} Billboard 100", user=user_id, public=False)
# print(create_playlist["id"])


spotipy_oath.user_playlist_add_tracks(
    user=user_id,
    playlist_id=create_playlist["id"],
    tracks=song_uris
)