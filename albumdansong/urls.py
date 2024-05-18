from albumdansong.views import create_album, list_album, list_album_label, create_lagu, list_lagu_label, cek_royalti, delete_album_label, list_lagu, detail_lagu
from albumdansong.views import delete_lagu, delete_album, delete_lagu_label
from django.urls import path

app_name = 'albumdansong'

urlpatterns = [
    path('create_album', create_album, name = 'create_album'),
    path('list_album_label', list_album_label, name = 'list_album_label'),
    path('list_album', list_album, name = 'list_album'),
    path('create_lagu/<str:id_album>', create_lagu, name = 'create_lagu'),
    path('list_lagu_label/<str:id_album>', list_lagu_label, name = 'list_lagu_label'),
    path('cek_royalti', cek_royalti, name = 'cek_royalti'),
    path('list_lagu/<str:id_album>', list_lagu, name = 'list_lagu'),
    path('detail_lagu/<str:id_lagu>', detail_lagu, name = 'detail_lagu'),
    path('delete_lagu/<str:id_album>/<str:id_lagu>', delete_lagu, name = 'delete_lagu'),
    path('delete_album/<str:id_album>', delete_album, name = 'delete_album'),
    path('delete_lagu_label/<str:id_album>/<str:id_lagu>', delete_lagu_label, name = 'delete_lagu_label'),
    path('delete_album_label/<str:id_album>', delete_album_label, name = 'delete_album_label'),

]