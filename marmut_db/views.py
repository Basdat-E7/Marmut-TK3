from django.shortcuts import render, redirect
from django.db.models import Q
import psycopg2
from Marmut_TK3 import settings
from .models import Song, Podcast, UserPlaylist, Akun, Label
from .forms import UserRegistrationForm, LabelRegistrationForm
from itertools import chain

def get_db_connection():
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    return conn

# Create your views here.
def show_main(request):
    
    return render(request, "dashboard.html")

def login(request):

    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marmut_db:show_main')  # Redirect to the main dashboard or any other page
        else:
            print(form.errors)  # Debugging: Print form errors to the terminal
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

def register_label(request):
    if request.method == 'POST':
        form = LabelRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marmut_db:show_main')  # Redirect to home page or any other page
    else:
        form = LabelRegistrationForm()
    return render(request, 'register_label.html', {'form': form})

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