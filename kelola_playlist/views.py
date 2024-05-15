from django.shortcuts import render
from django.db import connection
# from utils import query  # type: ignore

# Create your views here.
def tambah_playlist(request):
    return render(request, "tambah_playlist.html")

def show_playlist(request):
    return render(request, "user_playlist.html")

def detail_playlist(request):
    return render(request, "playlist_detail.html")

def tambah_lagu(request):
    return render(request, "tambah_lagu.html")

def play_song(request):
    return render(request, "play_song.html")

def add_song_to_playlist(request):
    return render(request, "add_song_to_user_playlist.html")


def testing(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Marmut.Genre")
        rows = cursor.fetchone()
        cursor.close()
    
    context = {
        'rows': rows,
    }

    return render(request, 'testdoangcok.html', context)
