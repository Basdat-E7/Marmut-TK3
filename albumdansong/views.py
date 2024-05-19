from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import *
import uuid

# Create your views here.
def create_album(request):
    email= request.session['email']

    # identify artis atau songwriter
    curr.execute("SELECT * FROM marmut.artist WHERE email_akun= %s", (email,))
    is_artist = curr.fetchone()

    curr.execute("SELECT * FROM marmut.songwriter WHERE email_akun= %s", (email,))
    is_songwriter = curr.fetchone()


    if request.method == 'POST':
        judul_album = request.POST.get('judul_album')
        id_label = request.POST.get('id_label')

        id_album = uuid.uuid4()

        judul_lagu = request.POST.get('judul_lagu')
        id_artis = request.POST.get('artist')
        id_songwriter = request.POST.getlist('songwriter')
        genre_res= request.POST.getlist('genre') 
        durasi = request.POST.get('durasi') 
        tanggal_hari_ini = datetime.now().date()
        tahun_saat_ini = datetime.now().year

        id_konten = uuid.uuid4()
        total_play= 0
        total_download = 0
        
        curr.execute("SELECT COUNT(*) AS jumlah_lagu FROM marmut.song WHERE id_album = %s", (id_album,))
        jumlah_lagu = curr.fetchone()

        curr.execute("INSERT INTO marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) VALUES (%s, %s, %s, %s, %s)", 
                     (id_album, judul_album, 1, id_label, durasi,) )
        
        curr.execute("INSERT INTO marmut.konten (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", 
                     (id_konten, judul_lagu, tanggal_hari_ini, tahun_saat_ini, durasi,))
        

        curr.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, %s, %s)", 
                         (id_konten, id_artis, id_album, total_play, total_download,))
        
        
        # for songwriter in id_songwriter:
        for songwriter_id in id_songwriter:
            curr.execute("INSERT INTO marmut.SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)", (songwriter_id, id_konten,))

        for genre in genre_res:
            curr.execute("INSERT INTO marmut.GENRE (id_konten, genre) VALUES (%s, %s)", (id_konten, genre,))
        
        pemilik_hak_ciptas = set()

        curr.execute("SELECT id_pemilik_hak_cipta FROM marmut.ARTIST WHERE id = %s", (id_artis,))
        pemilik_hak_cipta_artist = curr.fetchone()
        if pemilik_hak_cipta_artist not in pemilik_hak_ciptas:
            curr.execute(" INSERT INTO marmut.ROYALTI (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)", 
                         (pemilik_hak_cipta_artist, id_konten))
            pemilik_hak_ciptas.add(pemilik_hak_cipta_artist)
        

        for songwriter in id_songwriter:
            print(songwriter)
            curr.execute("SELECT id_pemilik_hak_cipta FROM marmut.SONGWRITER WHERE id = %s", (songwriter,))
            pemilik_hak_cipta_songwriter = curr.fetchone()

            if pemilik_hak_cipta_songwriter not in pemilik_hak_ciptas:
                curr.execute(" INSERT INTO marmut.ROYALTI (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)", 
                             (pemilik_hak_cipta_songwriter, id_konten))
                pemilik_hak_ciptas.add(pemilik_hak_cipta_songwriter)
        
        connection.commit()
        return redirect("albumdansong:list_album")
    
    curr.execute("SELECT nama, id FROM marmut.label")
    results = curr.fetchall()
    labels = []
    for result in results:
        label = {
            'nama': result[0],
            'id': result[1] 
        }
    labels.append(label)
    # print(results[1])
    
    akun_artis = None
    akun_songwriter = None
    nama_artis_login = None
    nama_songwriter_login = None

    if is_artist is not None:
        curr.execute("SELECT ak.nama, ar.id FROM marmut.akun AS ak JOIN marmut.artist AS ar ON ak.email = ar.email_akun WHERE ak.email = %s", (email,))
        nama_artis_login = curr.fetchone()
        akun_artis = {
            'nama': nama_artis_login[0],
            'id' : nama_artis_login[1]
        }
    
    if is_songwriter is not None:
        curr.execute("SELECT ak.nama, sw.id FROM marmut.akun AS ak JOIN marmut.songwriter AS sw ON ak.email = sw.email_akun WHERE ak.email = %s", (email,))
        nama_songwriter_login = curr.fetchone()
        akun_songwriter= {
            'nama': nama_songwriter_login[0],
            'id': nama_songwriter_login[1]
            }
        # print(nama_songwriter_login)

    

    curr.execute("SELECT u.nama, ar.id FROM marmut.AKUN u JOIN marmut.ARTIST ar ON u.email = ar.email_akun")
    artists = curr.fetchall()
    artist_result = [
        {
            'nama': artist[0], 
            'id': artist[1], 
        } for artist in artists
    ]

    curr.execute(" SELECT u.nama, sw.id FROM marmut.AKUN u JOIN marmut.SONGWRITER sw ON u.email = sw.email_akun")
    songwriters = curr.fetchall()
    # print(songwriters)
    songwriter_result = [
        # {
        #     'nama': sw[0], 
        #     'id': sw[1], 
        # } for sw in songwriters
    ]
    curr.execute("SELECT DISTINCT genre FROM marmut.GENRE")
    genres = curr.fetchall()
    # print(genres)
    # genre_result = [
    #     {
    #         'jenis': genre[0]
    #     } for genre in genres
    # ]    

    context = {
        'akun_artis' : akun_artis,
        'nama_artis_login': nama_artis_login,
        'akun_songwriter': akun_songwriter,
        'nama_songwriter_login' : nama_songwriter_login,
        'artists': artists,
        'songwriter_result': songwriter_result,
        'songwriters': songwriters,
        'genres' : genres,
        'labels' : labels,
        'results' : results

    }
    return render(request, "create_album.html", context)

def list_album(request):
    email= request.session['email']
    curr.execute("SELECT * FROM marmut.artist WHERE email_akun= %s", (email,))
    is_artist = curr.fetchone()

    curr.execute("SELECT * FROM marmut.songwriter WHERE email_akun= %s", (email,))
    is_songwriter = curr.fetchone()

    curr.execute("SELECT id FROM marmut.songwriter WHERE email_akun = %s", (email,))
    id_songwriter= curr.fetchone()

    if is_songwriter is not None:
    
        curr.execute(
            '''
            SELECT DISTINCT
                    al.judul AS judul_album,
                    al.jumlah_lagu,
                    al.total_durasi,
                    al.id AS id_album,
                    l.nama AS nama_label
                FROM 
                    marmut.album AS al
                LEFT JOIN
                    marmut.song AS s ON s.id_album = al.id
                LEFT JOIN 
                    marmut.songwriter_write_song AS sws ON sws.id_song = s.id_konten
                LEFT JOIN 
                    marmut.songwriter as sw ON sw.id = sws.id_songwriter
                LEFT JOIN 
                    marmut.label AS l ON al.id_label = l.id
                LEFT JOIN 
                    marmut.akun as ak ON ak.email = sw.email_akun
                WHERE 
                    ak.email = %s
            ''', (email,)
        )
        albumz = curr.fetchall()

    if is_artist is not None:
        curr.execute(
            '''
            SELECT DISTINCT
                    al.judul AS judul_album,
                    al.jumlah_lagu,
                    al.total_durasi,
                    al.id AS id_album,
                    l.nama AS nama_label
                FROM 
                    marmut.album AS al
                LEFT JOIN
                    marmut.song AS s ON s.id_album = al.id
                LEFT JOIN 
                    marmut.artist AS ar ON s.id_artist = ar.id
                LEFT JOIN 
                    marmut.label AS l ON al.id_label = l.id
                LEFT JOIN 
                    marmut.akun as ak ON ak.email = ar.email_akun
                WHERE 
                    ak.email = %s
            ''', (email,)
        )
        albumz = curr.fetchall()
    print(albumz)
    return render(request, "list_album.html", {'albumz': albumz})

def create_lagu(request, id_album):
    email= request.session['email']
    curr.execute("SELECT * FROM marmut.artist WHERE email_akun= %s", (email,))
    is_artist = curr.fetchone()

    curr.execute("SELECT * FROM marmut.songwriter WHERE email_akun= %s", (email,))
    is_songwriter = curr.fetchone()

    if request.method == 'POST':
        id_album_now = id_album
        judul_lagu = request.POST.get('judul')
        id_artis = request.POST.get('artist')
        id_songwriter = request.POST.getlist('songwriter')
        genre_res= request.POST.getlist('genre') 
        durasi = request.POST.get('durasi') 
        tanggal_hari_ini = datetime.now().date()
        tahun_saat_ini = datetime.now().year
        id_konten = uuid.uuid4()
        total_play= 0
        total_download = 0
        curr.execute("INSERT INTO marmut.konten (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)", 
                     (id_konten, judul_lagu, tanggal_hari_ini, tahun_saat_ini, durasi,))
        
        curr.execute("INSERT INTO marmut.song (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, %s, %s)", 
                         (id_konten, id_artis, id_album_now, total_play, total_download,))
        
        for songwriter_id in id_songwriter:
            curr.execute("INSERT INTO marmut.SONGWRITER_WRITE_SONG (id_songwriter, id_song) VALUES (%s, %s)", (songwriter_id, id_konten,))

        for genre in genre_res:
            curr.execute("INSERT INTO marmut.GENRE (id_konten, genre) VALUES (%s, %s)", (id_konten, genre,))
        
        pemilik_hak_ciptas = set()

        curr.execute("SELECT id_pemilik_hak_cipta FROM marmut.ARTIST WHERE id = %s", (id_artis,))
        pemilik_hak_cipta_artist = curr.fetchone()
        if pemilik_hak_cipta_artist not in pemilik_hak_ciptas:
            curr.execute(" INSERT INTO marmut.ROYALTI (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)", 
                         (pemilik_hak_cipta_artist, id_konten))
            pemilik_hak_ciptas.add(pemilik_hak_cipta_artist)
        

        for songwriter in id_songwriter:
            print(songwriter)
            curr.execute("SELECT id_pemilik_hak_cipta FROM marmut.SONGWRITER WHERE id = %s", (songwriter,))
            pemilik_hak_cipta_songwriter = curr.fetchone()

            if pemilik_hak_cipta_songwriter not in pemilik_hak_ciptas:
                curr.execute(" INSERT INTO marmut.ROYALTI (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)", 
                             (pemilik_hak_cipta_songwriter, id_konten))
                pemilik_hak_ciptas.add(pemilik_hak_cipta_songwriter)
        
        curr.execute("SELECT COUNT(*) FROM marmut.song WHERE id_album = %s", (id_album,))
        jumlah_lagu = curr.fetchone()
        
        curr.execute(
            """
                SELECT SUM(k.durasi) AS total_duration
                FROM marmut.Album as al
                JOIN marmut.Song as s ON al.id = s.id_album
                JOIN marmut.konten as k ON s.id_konten = k.id
                WHERE al.id = %s
            """, (id_album,)
        )
        total_durasi = curr.fetchone()
        curr.execute("UPDATE marmut.ALBUM SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s", (jumlah_lagu, total_durasi,  id_album,))

        connection.commit()
        return redirect("albumdansong:list_lagu", id_album=id_album)

    nama_artis_login = None
    nama_songwriter_login = None

    if is_artist is not None:
        curr.execute("SELECT ak.nama, ar.id FROM marmut.akun AS ak JOIN marmut.artist AS ar ON ak.email = ar.email_akun WHERE ak.email = %s", (email,))
        nama_artis_login = curr.fetchone()
    
    if is_songwriter is not None:
        curr.execute("SELECT ak.nama, sw.id FROM marmut.akun AS ak JOIN marmut.songwriter AS sw ON ak.email = sw.email_akun WHERE ak.email = %s", (email,))
        nama_songwriter_login = curr.fetchone()

    curr.execute("SELECT u.nama, ar.id FROM marmut.AKUN u JOIN marmut.ARTIST ar ON u.email = ar.email_akun")
    artists = curr.fetchall()
    curr.execute(" SELECT u.nama, sw.id FROM marmut.AKUN u JOIN marmut.SONGWRITER sw ON u.email = sw.email_akun")
    songwriters = curr.fetchall()
    curr.execute("SELECT DISTINCT genre FROM marmut.GENRE")
    genres = curr.fetchall()

    curr.execute("SELECT judul FROM marmut.ALBUM WHERE id = %s", (id_album,))
    judul_album = curr.fetchone()
    context = {
        'nama_artis_login': nama_artis_login,
        'nama_songwriter_login' : nama_songwriter_login,
        'artists': artists,
        'songwriters': songwriters,
        'genres' : genres,
        'judul_album': judul_album,
        'id_album': id_album

    }

    return render(request, "create_lagu.html", context)

def list_lagu(request, id_album):
    curr.execute(
        '''
            SELECT 
                k.judul, k.durasi, k.id,
                s.id_album, s.total_play, s.total_download
            FROM 
                marmut.konten AS k
            LEFT JOIN 
                marmut.song AS s ON k.id = s.id_konten
            WHERE 
                s.id_album = %s
            ''', (id_album,)
    )
    songs = curr.fetchall()
    return render(request, "list_lagu.html", {'songs': songs})

def list_album_label(request):
    email= request.session['email']
    curr.execute("SELECT id FROM marmut.label WHERE email = %s", (email,))
    id_label = curr.fetchone()

    curr.execute("SELECT DISTINCT judul, jumlah_lagu, total_durasi, id FROM marmut.album where id_label= %s", (id_label,))
    albums = curr.fetchall()


    return render(request, "list_album_label.html", {'albums': albums })

def list_lagu_label(request, id_album):
    # id_album= request.session['id_album']
    curr.execute(
        '''
            SELECT 
                k.judul, k.durasi, k.id,
                s.id_album, s.total_play, s.total_download
            FROM 
                marmut.konten AS k
            LEFT JOIN 
                marmut.song AS s ON k.id = s.id_konten
            WHERE 
                s.id_album = %s
            ''', (id_album,)
    )
    songs = curr.fetchall()
    return render(request, "list_lagu_label.html", {'songs': songs})

def detail_lagu (request, id_lagu):
    curr.execute("""
            SELECT K.judul, K.tanggal_rilis, K.tahun, K.durasi, S.total_play, S.total_download
            FROM marmut.konten AS K
            JOIN marmut.song AS S ON S.id_konten = K.id
            WHERE K.id = %s
        """, (id_lagu,))
    detail = curr.fetchone()
    # print(detail)

    curr.execute("""SELECT Ak.nama
                    FROM marmut.artist AS Ar, marmut.akun AS Ak, marmut.song AS S
                    WHERE S.id_artist=Ar.id AND Ar.email_akun=Ak.email AND S.id_konten=%s""", (id_lagu,))
    artist=curr.fetchone()

    curr.execute("""SELECT DISTINCT Ak.nama
                    FROM marmut.songwriter AS S, marmut.songwriter_write_song AS SWS,
                    marmut.konten AS K, marmut.akun AS Ak
                    WHERE SWS.id_song=%s AND SWS.id_songwriter=S.id AND S.email_akun=Ak.email"""
    ,(id_lagu,))
    songwriter=curr.fetchall()

    curr.execute("""SELECT A.judul
                FROM marmut.album AS A, marmut.song AS S
                WHERE S.id_konten=%s AND S.id_album=A.id"""
    ,(id_lagu,))
    album=curr.fetchone()

    curr.execute("""SELECT G.genre
                FROM marmut.genre AS G, marmut.konten AS K
                WHERE G.id_konten=%s AND G.id_konten=K.id"""
    ,(id_lagu,))
    genre=curr.fetchall()

    curr.execute("""SELECT K.id
            FROM marmut.konten AS K, marmut.SONG AS S
            WHERE S.id_konten=%s AND S.id_konten=K.id"""
    ,(id_lagu,))
    id_get=curr.fetchone()

    context = {
        'detail_a':detail,
        'detail_b':artist,
        'detail_c':songwriter,
        'detail_d':album,
        'detail_e':genre,
        'get_id':id_get
    }

    return render(request, "detail_lagu.html", context)

def cek_royalti(request):
    email = request.session['email']

    # curr.execute("SELECT id FROM marmut.artist WHERE id IN (SELECT id FROM marmut.akun WHERE email_akun = %s", 
    #              (email,))
    # is_artist = curr.fetchone()

    # curr.execute("SELECT id FROM marmut.songwriter WHERE id IN (SELECT id FROM marmut.akun WHERE email_akun = %s", 
    #              (email,))
    # is_songwriter = curr.fetchone()

    # curr.execute("SELECT id FROM marmut.label WHERE id IN (SELECT id FROM marmut.akun WHERE email_akun = %s", 
    #              (email,))
    # is_label = curr.fetchone()

    # if is_artist or is_songwriter or is_label:
    curr.execute(
            '''SELECT 
                    k.judul AS judul_lagu, 
                    a.judul AS judul_album, 
                    s.total_play, 
                    s.total_download, 
                    (phc.rate_royalti * s.total_download) AS total_royalti_didapat
                FROM 
                    marmut.konten AS k
                LEFT JOIN 
                    marmut.song AS s ON k.id = s.id_konten
                LEFT JOIN 
                    marmut.album AS a ON s.id_album = a.id
                LEFT JOIN 
                    marmut.artist AS ar ON s.id_artist = ar.id
                LEFT JOIN 
                    marmut.pemilik_hak_cipta AS phc ON ar.id_pemilik_hak_cipta = phc.id
                WHERE 
                    ar.email_akun = %s ''', (email,))
    royalties = curr.fetchall()
    # print(royalties)
    return render(request, 'cek_royalti.html', {'royalties': royalties})

def delete_lagu_q(id_lagu):
    curr.execute("DELETE FROM marmut.royalti WHERE id_song = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.songwriter_write_song WHERE id_song = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.genre WHERE id_konten = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.akun_play_song WHERE id_song = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.downloaded_song WHERE id_Song = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.song WHERE id_konten = %s", (id_lagu,))
    curr.execute("DELETE FROM marmut.konten WHERE id = %s", (id_lagu,))
    connection.commit()

def delete_lagu(request, id_album, id_lagu):

    delete_lagu_q(id_lagu)
    curr.execute("SELECT COUNT(*) FROM marmut.song WHERE id_album = %s", (id_album,))
    jumlah_lagu = curr.fetchone()
        
    curr.execute(
            """
                SELECT SUM(k.durasi) AS total_duration
                FROM marmut.Album as al
                JOIN marmut.Song as s ON al.id = s.id_album
                JOIN marmut.konten as k ON s.id_konten = k.id
                WHERE al.id = %s
            """, (id_album,)
        )
    total_durasi = curr.fetchone()
    curr.execute("UPDATE marmut.ALBUM SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s", (jumlah_lagu, total_durasi,  id_album,))
    connection.commit()
    return redirect('albumdansong:list_album')

def delete_lagu_label(request, id_album, id_lagu):

    delete_lagu_q(id_lagu)
    curr.execute("SELECT COUNT(*) FROM marmut.song WHERE id_album = %s", (id_album,))
    jumlah_lagu = curr.fetchone()
        
    curr.execute(
            """
                SELECT SUM(k.durasi) AS total_duration
                FROM marmut.Album as al
                JOIN marmut.Song as s ON al.id = s.id_album
                JOIN marmut.konten as k ON s.id_konten = k.id
                WHERE al.id = %s
            """, (id_album,)
        )
    total_durasi = curr.fetchone()
    curr.execute("UPDATE marmut.ALBUM SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s", (jumlah_lagu, total_durasi,  id_album,))
    connection.commit()
    return redirect('albumdansong:list_album_label')

def delete_album(request, id_album):
    curr.execute("SELECT id_konten FROM marmut.song WHERE id_album = %s", (id_album,))
    id_kontens = curr.fetchall()

    for id_konten in id_kontens:
        delete_lagu_q(id_konten)
    
    curr.execute("DELETE FROM marmut.album WHERE id = %s", (id_album,))
    return redirect("albumdansong:list_album")

def delete_album_label(request, id_album):
    curr.execute("SELECT id_konten FROM marmut.song WHERE id_album = %s", (id_album,))
    id_kontens = curr.fetchall()

    for id_konten in id_kontens:
        delete_lagu_q(id_konten)
    
    curr.execute("DELETE FROM marmut.album WHERE id = %s", (id_album,))
    return redirect("albumdansong:list_album_label")