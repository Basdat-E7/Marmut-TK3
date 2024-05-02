from albumdansong.views import create_album, list_album, list_album_label, create_lagu_songwriter, create_lagu_artist, list_lagu, cek_royalti
from django.urls import path

app_name = 'albumdansong'

urlpatterns = [
    path('create_album', create_album, name = 'create_album'),
    path('list_album', list_album, name = 'list_album'),
    path('list_album_label', list_album_label, name = 'list_album_label'),
    path('create_lagu', create_lagu_songwriter, name = 'create_lagu'),
    path('create_lagu_artist', create_lagu_artist, name = 'create_lagu_artist'),
    path('list_lagu', list_lagu, name = 'list_lagu'),
    path('cek_royalti', cek_royalti, name = 'cek_royalti'),
]