from django.urls import path
from kelola_playlist.views import *


app_name = 'kelola_playlist'

urlpatterns = [
    path('', show_playlists, name='show_playlists'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('ubah_playlist/<str:id_playlist>/', ubah_playlist, name='ubah_playlist'),
    path('delete_playlist/<str:id_playlist>/', delete_playlist, name='delete_playlist'),
    path('detail_playlist/<str:id_playlist>/', detail_playlist, name='detail_playlist'),
    path('detail_playlist/<str:id_playlist>/tambah_lagu/', tambah_lagu, name='tambah_lagu'),
    path('detail_playlist/<str:id_playlist>/<str:id_user_playlist>/shuffle/', shuffle_play, name="shuffle_play"),
    path('detail_playlist/<str:id_playlist>/<str:id_song>/delete/',delete_song, name="delete_song"),
    path('detail_playlist/<str:id_playlist>/<str:id_song>/play_song/', play_song, name='play_song'),
    path('detail_song/<str:id_song>/', detail_song, name='detail_song'),
    path('detail_song/<str:id_song>/slider_play/', slider_play, name='slider_play'),
    path('detail_song/<str:id_song>/download_song/',download_song, name="download_song"),
    path('detail_song/<str:id_song>/add_song_to_playlist/', add_song_to_playlist, name='add_song_to_user_playlist'),
]
