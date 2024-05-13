from django.shortcuts import render

# Create your views here.
def create_album(request):
    return render(request, "create_album.html")

def list_album(request):
    return render(request, "list_album.html")

def list_album_label(request):
    return render(request, "list_album_label.html")

def create_lagu_songwriter(request):
    return render(request, "create_lagu.html")

def create_lagu_artist(request):
    return render(request, "create_lagu_artist.html")

def list_lagu(request):
    return render(request, "list_lagu.html")

def cek_royalti(request):
    return render(request, "cek_royalti.html")
