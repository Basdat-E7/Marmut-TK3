from django.urls import path
from kelola_playlist.views import *


app_name = 'kelola_playlist'

urlpatterns = [
    path('', show_playlist, name='show_playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('detail_playlist/', detail_playlist, name='playlist_detail'),
    path('detail_playlist/tambah_lagu/', tambah_lagu, name='tambah_lagu'),
    path('detail_playlist/play_song/', play_song, name='play_song'),
    path('detail_playlist/play_song/add_song_to_playlist', add_song_to_playlist, name='add_song_to_user_playlist')
]
