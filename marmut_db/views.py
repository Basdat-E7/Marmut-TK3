from django.shortcuts import render, redirect
from django.db.models import Q
import psycopg2
from Marmut_TK3 import settings
from .models import Song, Podcast, UserPlaylist, Akun, Label
from .forms import UserRegistrationForm, LabelRegistrationForm, LoginForm
from itertools import chain
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import datetime

from utils.query import *
import uuid

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
    if request.method == 'POST':
        # Ambil data yang di-submit dari form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Coba melakukan autentikasi menggunakan username (email) dan password
        user, is_premium, roles = authenticate_akun(username, password)

        # Jika autentikasi berhasil, loginkan user dan redirect ke halaman utama
        if user is not None:
            request.session['username'] = username
            request.session['premium_status'] = 'Premium' if is_premium else 'Free'
            request.session['roles'] = roles

            if 'Label' in roles:
                request.session['name'] = user[1]
                request.session['email'] = user[2]
                request.session['contact'] = user[4]
            elif 'Akun' in roles:
                request.session['name'] = user[2]
                request.session['email'] = user[0]
                request.session['birthplace'] = user[4]
                birthdate_string = user[5].strftime("%d-%m-%Y")
                request.session['birthdate'] = birthdate_string
                request.session['city'] = user[7]
                if user[3] == 0:
                    request.session['gender'] = "Perempuan"
                else:
                    request.session['gender'] = "Laki-laki"
                if 'Artist' in roles:
                    request.session['songs'] = get_songs_by_artist(username)
                elif 'Songwriter' in roles:
                    request.session['songs'] = get_songs_by_songwriter(username)
                elif 'Artist' and 'Songwriter' in roles:
                    request.session['songs'] = get_songs_by_artist(username) + get_songs_by_songwriter(username)
                elif 'Podcaster' in roles:
                    request.session['podcasts'] = get_podcasts_by_podcaster(username)
            return redirect('marmut_db:show_main')
        else:
            # Jika autentikasi gagal, tampilkan pesan error
            error_message = 'Invalid username or password'
            print(error_message)
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def authenticate_akun(username, password):
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

    try:
        # Buat cursor untuk melakukan query
        cur = conn.cursor()
        
        # Cek di tabel akun
        cur.execute("SELECT * FROM marmut.akun WHERE email = %s", (username,))
        akun = cur.fetchone()
        
        # print(f"Result from 'akun' table: {akun}")
        # Cek di tabel label jika tidak ditemukan di tabel akun
        if not akun:
            print("User not found in 'akun', checking 'label' table")
            cur.execute("SELECT * FROM marmut.label WHERE email = %s", (username,))
            label = cur.fetchone()
            # print(f"Result from 'label' table: {label}")
            if label and label[3] == password:
                user = label
                role = 'Label'
            else:
                user = None
                role = None
        else:
            if akun[1] == password:
                user = akun
                role = 'Akun'
            else:
                user = None
                role = None

        if user:
            # Cek status premium
            cur.execute("SELECT * FROM marmut.premium WHERE email = %s", (username,))
            premium_status = cur.fetchone()

            # Cek apakah pengguna memiliki langganan premium yang berakhir
            if premium_status:
                premium_id = premium_status[0]
                # Periksa apakah langganan premium telah berakhir
                cur.execute("SELECT * FROM marmut.transaction WHERE email = %s AND timestamp_berakhir < CURRENT_DATE", (username,))
                expired_premium = cur.fetchone()
                print(expired_premium)
                if expired_premium:
                    # Jika langganan premium telah berakhir, hapus dari tabel premium
                    cur.execute("DELETE FROM marmut.downloaded_song WHERE email_downloader = %s", (premium_id,))
                    cur.execute("DELETE FROM marmut.premium WHERE email = %s", (premium_id,))
                    conn.commit()
                    # Set status premium menjadi False
                    premium_status = None

            # Cek roles
            roles = []
            if role == 'Akun':
                roles.append('Akun')
                cur.execute("SELECT * FROM marmut.artist WHERE email_akun = %s", (username,))
                if cur.fetchone():
                    roles.append('Artist')
                
                cur.execute("SELECT * FROM marmut.songwriter WHERE email_akun = %s", (username,))
                if cur.fetchone():
                    roles.append('Songwriter')
                
                cur.execute("SELECT * FROM marmut.podcaster WHERE email = %s", (username,))
                if cur.fetchone():
                    roles.append('Podcaster')
            else:
                roles.append('Label')

            cur.close()
            conn.close()

            return user, premium_status is not None, roles
        else:
            cur.close()
            conn.close()
            return None, False, []
    except psycopg2.Error as e:
        # Tangani kesalahan koneksi atau query
        print("Error:", e)
        return None, False, []

def get_songs_by_artist(username):
    
    # Mengambil id_artis berdasarkan email_akun
    curr.execute("SELECT id FROM marmut.artist WHERE email_akun = %s", (username,))
    artist_id = curr.fetchone()[0]

    # Mengambil lagu yang dimiliki oleh artis berdasarkan id_artis
    curr.execute("""
        SELECT konten.judul
        FROM marmut.song
        INNER JOIN marmut.konten ON song.id_konten = konten.id
        WHERE song.id_artist = %s
    """, (artist_id,))
    songs = [row[0] for row in curr.fetchall()]
    print(songs)
    return songs
        

def get_songs_by_songwriter(username):
    curr.execute("SELECT id FROM marmut.songwriter WHERE email_akun = %s", (username,))
    songwriter_id = curr.fetchone()[0]

    curr.execute("SELECT id_song FROM marmut.songwriter_write_song WHERE id_songwriter = %s", (songwriter_id,))
    song_ids = [row[0] for row in curr.fetchall()]

    song_titles = []
    for song_id in song_ids:
        curr.execute("""
            SELECT konten.judul
            FROM marmut.song
            INNER JOIN marmut.konten ON song.id_konten = konten.id
            WHERE song.id_konten = %s
        """, (song_id,))
        song_title = curr.fetchone()[0]
        song_titles.append(song_title)
        print(song_titles)
    return song_titles

def get_podcasts_by_podcaster(username):
    # Mendapatkan id_podcaster berdasarkan email
    curr.execute("SELECT email FROM marmut.podcaster WHERE email = %s", (username,))
    podcaster_id = curr.fetchone()[0]

    # Mendapatkan id_konten dari podcast yang di-host oleh podcaster tersebut
    curr.execute("SELECT id_konten FROM marmut.podcast WHERE email_podcaster = %s", (podcaster_id,))
    id_konten_list = curr.fetchall()

    # Mendapatkan judul podcast berdasarkan id_konten
    podcast_titles = []
    for id_konten in id_konten_list:
        curr.execute("SELECT judul FROM marmut.konten WHERE id = %s", (id_konten,))
        title = curr.fetchone()[0]
        podcast_titles.append(title)

    return podcast_titles

def register(request):
    return render(request, "register.html")

def logout(request):
    # Clear the session data
    request.session.flush()
    # Redirect to the login page or homepage
    return redirect('marmut_db:show_main')

def register_user(request):
    if "username" in request.session:
        return redirect("marmut_db:show_main")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        gender_int = 0 if gender == "female" else 1
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        artist = request.POST.get('is_artist', False)
        songwriter = request.POST.get('is_songwriter', False)
        podcaster = request.POST.get('is_podcaster', False)

        is_verified = artist or songwriter or podcaster
        id_pemilik_hak_cipta = str(uuid.uuid4())

        # cek username exist ga
        exist = curr.execute("SELECT * FROM marmut.akun WHERE email = %s", (email,))
        result = curr.fetchone()
        if result is not None:
            messages.error(request, "Email already taken. Please choose another email.")
            return redirect("marmut_db:register_user")
        else:
            curr.execute("INSERT INTO marmut.AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                         (email, password, nama, gender_int, tempat_lahir, tanggal_lahir, is_verified, kota_asal,))
            if podcaster:
                curr.execute( "INSERT INTO marmut.PODCASTER (email) VALUES (%s)", (email,))
            if artist or songwriter:
                rate_royalti = 0
                curr.execute("INSERT INTO marmut.PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", 
                             (id_pemilik_hak_cipta, rate_royalti,))
            
            if artist:  
                id_artist = str(uuid.uuid4())
                curr.execute("INSERT INTO marmut.ARTIST (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)", 
                             (id_artist, email, id_pemilik_hak_cipta,))

            if songwriter:
                id_songwriter = str(uuid.uuid4())
                curr.execute("INSERT INTO marmut.ARTIST (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)", 
                             (id_songwriter, email, id_pemilik_hak_cipta,))
            
            
            
            #insert into database
            connection.commit()
            
            return redirect("marmut_db:show_main")
        
    return render(request, 'register_user.html')
            


#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             print(f"Email length: {len(cleaned_data['email'])}")
#             print(f"Password length: {len(cleaned_data['password'])}")
#             print(f"Nama length: {len(cleaned_data['nama'])}")
#             print(f"Tempat Lahir length: {len(cleaned_data['tempat_lahir'])}")
#             print(f"Kota Asal length: {len(cleaned_data['kota_asal'])}")
#             form.save()
#             return redirect('show_main')
#         else:
#             print(form.errors)
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register_user.html', {'form': form})

def register_label(request):
    if "username" in request.session:
        return redirect("marmut_db:show_main")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
    
        id_label = str(uuid.uuid4())
        id_pemilik_hak_cipta = str(uuid.uuid4())

        exist = curr.execute("SELECT * FROM marmut.label WHERE email = %s", (email,))
        result = curr.fetchone()

        if result is not None:
                messages.error(request, "Email already taken. Please choose another email.")
                return redirect("marmut_db:register_label")
            
        else:
            rate_royalti = 0
            curr.execute("INSERT INTO marmut.PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES (%s, %s)", 
                             (id_pemilik_hak_cipta, rate_royalti,))
            
            curr.execute("INSERT INTO marmut.LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES (%s, %s, %s, %s, %s, %s)", 
                         (id_label, nama, email, password, kontak, id_pemilik_hak_cipta))
            
            connection.commit()
            
            return redirect("marmut_db:show_main")
        
    return render(request, 'register_label.html')

    # if request.method == 'POST':
    #     form = LabelRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('marmut_db:show_main')  # Redirect to home page or any other page
    # else:
    #     form = LabelRegistrationForm()
    # return render(request, 'register_label.html', {'form': form})

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