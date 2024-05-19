from django.shortcuts import render
from utils.query import *
import uuid
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse

# Create your views here.
def tambah_playlist(request):
    if request.method == "POST":
        # try:
            judul_playlist = request.POST.get('title', '')  
            deskripsi_playlist = request.POST.get('description', '')
            email = request.session.get('email', '')
            id_playlist = str(uuid.uuid4())
            id_user_playlist = str(uuid.uuid4())
            timestamp_now = datetime.now().strftime('%Y-%m-%d')

            add_playlist = """INSERT INTO marmut.PLAYLIST (id) VALUES(%s)"""
            curr.execute(add_playlist, (id_playlist,))
            connection.commit()

            add_user_playlist = """INSERT INTO marmut.USER_PLAYLIST 
                                (email_pembuat, id_user_playlist, judul, deskripsi, 
                                jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            curr.execute(add_user_playlist, (email, id_user_playlist, judul_playlist, deskripsi_playlist, 0, timestamp_now, id_playlist, 0))
            connection.commit()

            return HttpResponseRedirect(reverse('kelola_playlist:show_playlists'))

        # except Exception as e:
        #     connection.rollback()
            
        #     messages.error(request, f"Failed to add playlist: {str(e)}")

        #     return HttpResponseRedirect(reverse('kelola_playlist:tambah_playlist'))

    return render(request, "tambah_playlist.html")

def show_playlists(request):
    email = request.session.get('email', '')
    
    query = """SELECT judul, jumlah_lagu, total_durasi,
            id_user_playlist, id_playlist 
            FROM marmut.user_playlist as U
            WHERE U.email_pembuat=%s"""
    curr.execute(query, (email,))
    rows = curr.fetchall()
    
    context = {
        'rows' : rows
    }

    return render(request, "user_playlist.html", context)

def detail_playlist(request, id_playlist):
    # try:
    query_songs = """SELECT DISTINCT K.judul, Ak.nama, K.durasi, PS.id_song
            FROM marmut.PLAYLIST_SONG AS PS
            JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
            JOIN marmut.KONTEN AS K ON S.id_konten = K.id
            JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
            JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
            WHERE PS.id_playlist = %s"""
    
    curr.execute(query_songs, (id_playlist,))
    songses = curr.fetchall()

    query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM marmut.PLAYLIST_SONG AS PS
                        JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                        JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                        JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
    curr.execute(query_jumlah_songs, (id_playlist,))
    amount_songs = curr.fetchone()

    query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM marmut.PLAYLIST_SONG AS PS
                            JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                            JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                            JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
    curr.execute(query_total_durasi, (id_playlist,))
    total_duration = curr.fetchone()

    jam = total_duration[0] // 60
    menit = total_duration[0] % 60

    query_details = """SELECT U.judul, U.jumlah_lagu, U.total_durasi, 
            U.tanggal_dibuat, U.deskripsi, U.id_playlist, A.nama,
            P.id_song, U.id_user_playlist
            FROM marmut.user_playlist AS U, marmut.akun AS A, 
            marmut.playlist_song AS P
            WHERE U.email_pembuat = A.email AND U.id_playlist=%s"""
    
    curr.execute(query_details, (id_playlist,))
    details = curr.fetchone()

    context = {
        'details': details,
        'songs': songses,
        'amount_songs':amount_songs,
        'total_duration':(jam,menit),
    }

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     context = {
    #         'rows': [],
    #         'songs': [],
    #         'amount_songs':[]
    #     }

    return render(request, "playlist_detail.html", context)

def ubah_playlist(request,id_playlist):

    ambil_id="""SELECT id_playlist
        FROM marmut.user_playlist
        WHERE id_playlist=%s"""
    curr.execute(ambil_id,(id_playlist,))
    id=curr.fetchone

    context={
        "id":id,
    }

    if request.method == "POST":

        judul_playlist = request.POST.get('title', '')  
        deskripsi_playlist = request.POST.get('description', '')


        edit_playlist = """UPDATE marmut.user_playlist
                        SET judul = %s, deskripsi = %s
                        WHERE id_playlist = %s"""
        curr.execute(edit_playlist, (judul_playlist,deskripsi_playlist,id_playlist))
        connection.commit()


        return HttpResponseRedirect(reverse('kelola_playlist:show_playlists'))

    return render(request, "ubah_playlist.html",context)

def delete_playlist(request,id_playlist):

    if request.method == "POST":

        delete_songs = "DELETE FROM marmut.playlist_song WHERE id_playlist=%s"
        curr.execute(delete_songs, (id_playlist,))

        delete_query = "DELETE FROM marmut.user_playlist WHERE id_playlist=%s"
        curr.execute(delete_query, (id_playlist,))

        delete_playlist_utama = "DELETE FROM marmut.playlist WHERE id=%s"
        curr.execute(delete_playlist_utama, (id_playlist,))

        connection.commit()
        return HttpResponseRedirect(reverse('kelola_playlist:show_playlists'))

    return render(request, "user_playlist.html")

def tambah_lagu(request, id_playlist):
    available_songs_query = """SELECT K.judul, U.nama, S.id_konten
                            FROM marmut.konten AS K, marmut.song AS S, 
                            marmut.akun AS U, marmut.artist AS A
                            WHERE K.id = S.id_konten AND S.id_artist = A.id AND 
                            A.email_akun = U.email"""
    curr.execute(available_songs_query)
    rows = curr.fetchall()

    ambil_id_query = """SELECT id_playlist
                        FROM marmut.user_playlist
                        WHERE id_playlist=%s"""
    
    curr.execute(ambil_id_query, (id_playlist,))
    id = curr.fetchone()

    

    context = {
        'rows': rows,
        'id': id,
        'error_message': None
    }

    if request.method == "POST":
        id_lagu = request.POST.get('id_lagu', '')

        # Cek apakah lagu sudah ada di playlist
        check_song_query = """SELECT 1 FROM marmut.playlist_song
                            WHERE id_playlist = %s AND id_song = %s"""
        curr.execute(check_song_query, (id_playlist, id_lagu))
        song_exists = curr.fetchone()

        if song_exists:
            # Lagu sudah ada di playlist, tampilkan pesan error
            context['error_message'] = "Lagu sudah ada di dalam playlist."
            return render(request, "tambah_lagu.html", context)
        else:
            # Lagu belum ada di playlist, tambahkan lagu
            add_song_query = """INSERT INTO marmut.playlist_song
                                (id_playlist, id_song)
                                VALUES (%s, %s)"""
            curr.execute(add_song_query, (id_playlist, id_lagu))
            connection.commit()

            query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM marmut.PLAYLIST_SONG AS PS
                        JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                        JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                        JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
            curr.execute(query_jumlah_songs, (id_playlist,))
            amount_songs = curr.fetchone()

            edit_jumlah_songs = """UPDATE marmut.user_playlist
                                SET jumlah_lagu = %s
                                WHERE id_playlist = %s"""
            curr.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
            connection.commit()

            query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM marmut.PLAYLIST_SONG AS PS
                            JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                            JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                            JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
            curr.execute(query_total_durasi, (id_playlist,))
            total_duration = curr.fetchone()

            edit_durasi_songs = """UPDATE marmut.user_playlist
                                SET total_durasi = %s
                                WHERE id_playlist = %s"""
            curr.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
            connection.commit()

            return HttpResponseRedirect(reverse('kelola_playlist:detail_playlist', args=(id_playlist,)))

    return render(request, "tambah_lagu.html", context)

def delete_song(request, id_playlist, id_song):
    if request.method == "POST":

        delete_query = "DELETE FROM marmut.playlist_song WHERE id_song=%s AND id_playlist=%s"
        curr.execute(delete_query, (id_song,id_playlist,))

        connection.commit()

        query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM marmut.PLAYLIST_SONG AS PS
                        JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                        JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                        JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
        curr.execute(query_jumlah_songs, (id_playlist,))
        amount_songs = curr.fetchone()

        edit_jumlah_songs = """UPDATE marmut.user_playlist
                            SET jumlah_lagu = %s
                            WHERE id_playlist = %s"""
        curr.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
        connection.commit()

        query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM marmut.PLAYLIST_SONG AS PS
                        JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                        JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                        JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
        curr.execute(query_total_durasi, (id_playlist,))
        total_duration = curr.fetchone()

        edit_durasi_songs = """UPDATE marmut.user_playlist
                            SET total_durasi = %s
                            WHERE id_playlist = %s"""
        curr.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
        connection.commit()
        return HttpResponseRedirect(reverse('kelola_playlist:detail_playlist', args=(id_playlist,)))

    return render(request, "playlist_detail.html")

def detail_song(request,id_song):
    email = request.session.get('email', '')

    check_premium = """SELECT 1 FROM marmut.premium
                            WHERE email=%s"""
    curr.execute(check_premium, (email,))
    premium_check = curr.fetchone()
    is_premium = premium_check is not None

    query_judul_song = """SELECT K.judul, K.tanggal_rilis, K.tahun, K.durasi, S.total_play,
                        S.total_download
                        FROM marmut.konten AS K, marmut.song AS S
                        WHERE S.id_konten = K.id AND K.id=%s"""
    curr.execute(query_judul_song, (id_song,))
    detail=curr.fetchone()

    query_artist = """SELECT Ak.nama
                    FROM marmut.artist AS Ar, marmut.akun AS Ak, marmut.song AS S
                    WHERE S.id_artist=Ar.id AND Ar.email_akun=Ak.email AND S.id_konten=%s"""
    curr.execute(query_artist, (id_song,))
    artist=curr.fetchone()

    query_songwriter="""SELECT DISTINCT Ak.nama
                    FROM marmut.songwriter AS S, marmut.songwriter_write_song AS SWS,
                    marmut.konten AS K, marmut.akun AS Ak
                    WHERE SWS.id_song=%s AND SWS.id_songwriter=S.id AND S.email_akun=Ak.email"""
    curr.execute(query_songwriter,(id_song,))
    songwriter=curr.fetchall()

    query_album="""SELECT A.judul
                FROM marmut.album AS A, marmut.song AS S
                WHERE S.id_konten=%s AND S.id_album=A.id"""
    curr.execute(query_album,(id_song,))
    album=curr.fetchone()

    query_genre="""SELECT G.genre
                FROM marmut.genre AS G, marmut.konten AS K
                WHERE G.id_konten=%s AND G.id_konten=K.id"""
    curr.execute(query_genre,(id_song,))
    genre=curr.fetchall()

    get_id="""SELECT K.id
            FROM marmut.konten AS K, marmut.SONG AS S
            WHERE S.id_konten=%s AND S.id_konten=K.id"""
    curr.execute(get_id,(id_song,))
    id_get=curr.fetchone()

    context = {
        'detail_a':detail,
        'detail_b':artist,
        'detail_c':songwriter,
        'detail_d':album,
        'detail_e':genre,
        'get_id':id_get,
        'is_premium':is_premium,
    }

    return render(request, "detail_song.html", context)

def slider_play(request, id_song):
    if request.method == "POST":

        email = request.session.get('email', '')
        timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        add_play  = """INSERT INTO marmut.akun_play_song 
                    (email_pemain, id_song, waktu) 
                    VALUES (%s, %s, %s)"""
        curr.execute(add_play, (email, id_song, timestamp_now))
        connection.commit()
        return HttpResponseRedirect(reverse('kelola_playlist:detail_song', args=(id_song,)))

    return render(request, "detail_song.html")

def add_song_to_playlist(request,id_song):

    query_judul_song = """SELECT K.judul
                        FROM marmut.konten AS K, marmut.song AS S
                        WHERE S.id_konten = K.id AND K.id=%s"""
    curr.execute(query_judul_song,(id_song,))
    deksripsi=curr.fetchone()

    query_penyanyi = """SELECT Ak.nama
                    FROM marmut.artist AS Ar, marmut.akun AS Ak, marmut.song AS S
                    WHERE S.id_artist=Ar.id AND Ar.email_akun=Ak.email AND S.id_konten=%s"""
    curr.execute(query_penyanyi, (id_song,))
    artist=curr.fetchone()

    email = request.session.get('email', '')

    query_pilihan = """SELECT U.judul, U.id_playlist
                    FROM marmut.user_playlist AS U
                    WHERE U.email_pembuat=%s"""
    curr.execute(query_pilihan, (email,))
    detail=curr.fetchall()

    get_id="""SELECT K.id
            FROM marmut.konten AS K, marmut.SONG AS S
            WHERE S.id_konten=%s AND S.id_konten=K.id"""
    curr.execute(get_id,(id_song,))
    id_get=curr.fetchone()

    context={
        'judul':deksripsi,
        'artist':artist,
        'playlists':detail,
        'id':id_get,
    }
    

    if request.method == "POST":

        id_playlist = request.POST.get('id_playlist', '')
        check_playlist = """SELECT judul
                        FROM marmut.user_playlist
                        WHERE id_playlist=%s"""
        curr.execute(check_playlist,(id_playlist,))
        judul_playlist = curr.fetchone()

        check_song_query = """SELECT 1 FROM marmut.playlist_song
                            WHERE id_playlist = %s AND id_song = %s"""
        curr.execute(check_song_query, (id_playlist, id_song))
        song_exists = curr.fetchone()

        if song_exists:
            # Lagu sudah ada di playlist, tampilkan pesan error
            context['error_message'] = "Lagu dengan judul " + deksripsi[0] + " sudah ada di playlist " + judul_playlist[0]
            return render(request, "add_song_to_user_playlist.html", context)
        else:
            context['success_message'] = f"{deksripsi[0]} berhasil ditambahkan ke playlist {judul_playlist[0]}"
            add_to_playlist = """INSERT INTO marmut.playlist_song
                                    (id_playlist, id_song) 
                                    VALUES (%s, %s)"""
            curr.execute(add_to_playlist, (id_playlist, id_song,))
            connection.commit()

            query_jumlah_songs = """SELECT COUNT(*)
                    FROM (
                        SELECT DISTINCT K.judul, Ak.nama, K.durasi
                        FROM marmut.PLAYLIST_SONG AS PS
                        JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                        JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                        JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                        JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                        WHERE PS.id_playlist = %s
                    ) AS subquery;
                    """
            curr.execute(query_jumlah_songs, (id_playlist,))
            amount_songs = curr.fetchone()

            edit_jumlah_songs = """UPDATE marmut.user_playlist
                                SET jumlah_lagu = %s
                                WHERE id_playlist = %s"""
            curr.execute(edit_jumlah_songs,(amount_songs[0],id_playlist,))
            connection.commit()

            query_total_durasi = """SELECT COALESCE(SUM(durasi), 0) AS total_durasi
                        FROM (
                            SELECT DISTINCT K.judul, Ak.nama, K.durasi
                            FROM marmut.PLAYLIST_SONG AS PS
                            JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
                            JOIN marmut.KONTEN AS K ON S.id_konten = K.id
                            JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
                            JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
                            WHERE PS.id_playlist = %s
                        ) AS subquery;
                        """
            curr.execute(query_total_durasi, (id_playlist,))
            total_duration = curr.fetchone()

            edit_durasi_songs = """UPDATE marmut.user_playlist
                                SET total_durasi = %s
                                WHERE id_playlist = %s"""
            curr.execute(edit_durasi_songs,(total_duration[0],id_playlist,))
            connection.commit()
            return render(request, "add_song_to_user_playlist.html",context)

    return render(request, "add_song_to_user_playlist.html",context)

def shuffle_play(request, id_playlist, id_user_playlist):
    if request.method == "POST":
        email = request.session.get('email', '')
        timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query_songs = """SELECT DISTINCT PS.id_song
            FROM marmut.PLAYLIST_SONG AS PS
            JOIN marmut.SONG AS S ON PS.id_song = S.id_konten
            JOIN marmut.KONTEN AS K ON S.id_konten = K.id
            JOIN marmut.ARTIST AS Ar ON S.id_artist = Ar.id
            JOIN marmut.akun AS Ak ON Ar.email_akun = Ak.email
            WHERE PS.id_playlist = %s"""
    
        curr.execute(query_songs, (id_playlist,))
        songses = curr.fetchall()

        play_playlist = """INSERT INTO marmut.akun_play_user_playlist
                        (email_pemain, id_user_playlist, email_pembuat, waktu)
                        VALUES (%s, %s, %s, %s)"""
        
        curr.execute(play_playlist, (email, id_user_playlist, email, timestamp_now,))
        connection.commit()

        play_all_songs = """INSERT INTO marmut.akun_play_song
                        (email_pemain, id_song, waktu)
                        VALUES (%s, %s, %s)"""
        for song in songses:
            curr.execute(play_all_songs, (email, song[0], timestamp_now,))
            connection.commit()

        return HttpResponseRedirect(reverse('kelola_playlist:detail_playlist', args=(id_playlist,)))
    
    return render(request, "playlist_detail.html")

def play_song(request,id_playlist, id_song):
    if request.method == "POST":
        email = request.session.get('email', '')
        timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        playing_song = """INSERT INTO marmut.akun_play_song 
                        (email_pemain, id_song, waktu) 
                        VALUES (%s, %s, %s)"""
        curr.execute(playing_song, (email, id_song, timestamp_now))
        connection.commit()

        return HttpResponseRedirect(reverse('kelola_playlist:detail_playlist', args=(id_playlist,)))

    return render(request, "playlist_detail.html")

def download_song(request, id_song):
    try:
        if request.method == "POST":
            email = request.session.get('email', '')

            downloader = """INSERT INTO marmut.downloaded_song
                            (id_song, email_downloader)
                            VALUES (%s, %s)"""
            curr.execute(downloader, (id_song, email,))
            connection.commit()
            messages.success(request, 'Berhasil mengunduh lagu.')

            return HttpResponseRedirect(reverse('kelola_playlist:detail_song', args=(id_song,)))
        
    except Exception as e:
        connection.rollback()

        messages.error(request, 'Gagal mengunduh lagu: ' + str(e))

        return HttpResponseRedirect(reverse('kelola_playlist:detail_song', args=(id_song,)))

    return render(request, "detail_song.html")