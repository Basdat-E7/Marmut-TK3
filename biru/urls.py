from django.urls import path
from biru.views import add_podcast, delete_podcast, podcast_detail, get_chart_details, podcaster, update_podcast

app_name = 'biru'
urlpatterns = [
    path('podcast_detail/<uuid:id_konten>', podcast_detail, name='podcast_detail'),
    path('chart/', get_chart_details, name='get_chart_details'),
    path('create_podcast/', add_podcast, name='create_podcast'),
    path('', podcaster, name='podcaster'),
    path('add_podcast/', add_podcast, name='add_podcast'),
    path('delete_podcast/<uuid:id_konten>', delete_podcast, name='delete_podcast'),
    path('update_podcast/<uuid:id_konten>', update_podcast, name='update_podcast'),
]