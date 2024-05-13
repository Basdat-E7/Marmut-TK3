from django.shortcuts import render
from django.db.models import Q
from .models import Song, Podcast, UserPlaylist
from itertools import chain

# Create your views here.
def show_main(request):
    
    return render(request, "dashboard.html")

def login(request):

    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def register_user(request):
    return render(request, "register_user.html")

def register_label(request):
    return render(request, "register_label.html")

def langganan_paket_page(request):
    return render(request, "langganan_paket.html")

def langganan_paket_submit(request):
    return render(request, "langganan_paket_submit.html")

def purchase_history(request):
    return render(request, "purchase_history.html")

def downloaded_songs(request):
    return render(request, "downloaded_songs.html")

def search(request):
    query = request.GET.get('q')
    if query:
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__name__icontains=query))
        podcasts = Podcast.objects.filter(Q(title__icontains=query) | Q(podcaster__name__icontains=query))
        playlists = UserPlaylist.objects.filter(Q(name__icontains=query) | Q(creator__name__icontains=query))
        results = list(chain(songs, podcasts, playlists))
    else:
        results = None
    return render(request, 'search_results.html', {'results': results})