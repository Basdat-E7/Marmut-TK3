from django.urls import path
from biru.views import podcast_detail, get_chart_details

app_name = 'biru'
urlpatterns = [
    path('podcast_detail/<uuid:id_konten>', podcast_detail, name='podcast_detail'),
    path('chart/', get_chart_details, name='get_chart_details'),
]