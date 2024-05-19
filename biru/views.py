from django.shortcuts import render, redirect
from django.db import OperationalError, ProgrammingError, connection
from django.http import HttpResponseNotFound, HttpResponse
from utils.query import *
import datetime, uuid
from django.contrib import messages

def format_durasi(menit):
    jam = menit // 60
    sisa_menit = menit % 60
    return f'{jam} jam {sisa_menit} menit' if jam > 0 else f'{sisa_menit} menit'

def format_durasi_dua(menit):
    if menit is None:
        return '0 jam 0 menit'
    else :
        jam = menit // 60
        sisa_menit = menit % 60
        if jam > 0:
            return f'{jam} jam {sisa_menit} menit'
        else :
            return f'{sisa_menit} menit'
        
# podcast detail
def podcast_detail(request, id_konten):
    # Fetch podcast details
    curr.execute("""
        SELECT K.judul, array_agg(G.genre), A.nama, K.durasi, K.tanggal_rilis, K.tahun
        FROM marmut.KONTEN K
        JOIN marmut.PODCAST P ON K.id = P.id_konten
        JOIN marmut.PODCASTER Po ON P.email_podcaster = Po.email
        JOIN marmut.AKUN A ON Po.email = A.email
        JOIN marmut.GENRE G ON K.id = G.id_konten
        WHERE K.id = %s
        GROUP BY K.judul, A.nama, K.durasi, K.tanggal_rilis, K.tahun
    """, [str(id_konten)])
    podcast = curr.fetchone()
    print(podcast)
    
    # Fetch podcast episodes
    curr.execute("""
        SELECT E.judul, E.deskripsi, E.durasi, E.tanggal_rilis
        FROM marmut.EPISODE E
        WHERE E.id_konten_podcast = %s
        ORDER BY E.tanggal_rilis DESC
    """, [str(id_konten)])
    episodes = curr.fetchall()
    print(episodes)

    return render(request, 'podcast_detail.html', {'podcast': podcast, 'episodes': episodes})

# crud kelola podcast
#def add_podcast(request):
#    if request.method == 'POST':
#        email = request.session.get('user_email', None)
#        judul = request.POST['judul']
#        genre = request.POST.getlist('genre')
#
#        # Buat UUID baru untuk podcast ini
#        id_konten = uuid.uuid4()
#
#        # Hitung durasi total dari semua episode
#        curr.execute("""
#            SELECT SUM(durasi)
#            FROM marmut.EPISODE
#            WHERE id_konten_podcast = %s
#        """, [id_konten])
#
#        durasi = curr.fetchone()[0] or 0
#
#        curr.execute("""
#            INSERT INTO marmut.KONTEN (id, judul, tanggal_rilis, tahun, durasi)
#            VALUES (%s, %s, CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), %s)
#            RETURNING id
#        """, [id_konten, judul, durasi])
#
#        id_konten = curr.fetchone()[0]
#
#        curr.execute("""
#            INSERT INTO marmut.PODCAST (id_konten, email_podcaster)
#            VALUES (%s, %s)
#        """, [id_konten, email])
#
#        for g in genre:
#            curr.execute("""
#                INSERT INTO marmut.GENRE (id_konten, genre)
#                VALUES (%s, %s)
#            """, [id_konten, g])
#        print(id_konten)
#        return redirect('biru:podcaster')
#
#    return render(request, 'create_podcast.html')

def add_podcast(request):
    if request.method == 'POST':
        email = request.session.get('user_email', None)
        judul = request.POST['judul']
        genre = request.POST.getlist('genre')

        # Inisialisasi koneksi dan kursor
        with connection.cursor() as curr:
            # Buat UUID baru untuk podcast ini
            id_konten = uuid.uuid4()

            # Hitung durasi total dari semua episode
            curr.execute("""
                SELECT SUM(durasi)
                FROM marmut.EPISODE
                WHERE id_konten_podcast = %s
            """, [id_konten])

            durasi = curr.fetchone()[0] or 0

            # Masukkan data ke tabel KONTEN
            curr.execute("""
                INSERT INTO marmut.KONTEN (id, judul, tanggal_rilis, tahun, durasi)
                VALUES (%s, %s, CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), %s)
                RETURNING id
            """, [id_konten, judul, durasi])

            id_konten = curr.fetchone()[0]

            # Masukkan data ke tabel PODCAST
            curr.execute("""
                INSERT INTO marmut.PODCAST (id_konten, email_podcaster)
                VALUES (%s, %s)
            """, [id_konten, email])

            # Masukkan data ke tabel GENRE
            for g in genre:
                curr.execute("""
                    INSERT INTO marmut.GENRE (id_konten, genre)
                    VALUES (%s, %s)
                """, [id_konten, g])
        print(id_konten)
        return redirect('biru:podcaster')

    return render(request, 'create_podcast.html')


def delete_podcast(request, id_konten):
    if request.method == 'POST':
        # Pertama, hapus semua genre yang terkait dengan podcast ini
        curr.execute("""
            DELETE FROM marmut.GENRE
            WHERE id_konten = %s
        """, [id_konten])

        # Kedua, hapus semua episode yang terkait dengan podcast ini
        curr.execute("""
            DELETE FROM marmut.EPISODE
            WHERE id_konten_podcast = %s
        """, [id_konten])

        # Ketiga, hapus podcast dari tabel PODCAST
        curr.execute("""
            DELETE FROM marmut.PODCAST
            WHERE id_konten = %s
        """, [id_konten])

        # Keempat, hapus konten dari tabel KONTEN
        curr.execute("""
            DELETE FROM marmut.KONTEN
            WHERE id = %s
        """, [id_konten])

        return redirect('biru:podcaster')

    else:
        # Handle non-POST requests here
        return render(request, 'create_podcast.html', {'message': 'Invalid request method'})

def update_podcast(request, id_konten):
    if request.method == 'POST':
        judul = request.POST['judul']
        genre = request.POST.getlist('genre')
        durasi = request.POST['durasi']

        # Update konten
        curr.execute("""
            UPDATE marmut.KONTEN
            SET judul = %s, durasi = %s
            WHERE id = %s
        """, [judul, durasi, id_konten])

        # Hapus genre lama
        curr.execute("""
            DELETE FROM marmut.GENRE
            WHERE id_konten = %s
        """, [id_konten])

        # Tambahkan genre baru
        for g in genre:
            curr.execute("""
                INSERT INTO marmut.GENRE (id_konten, genre)
                VALUES (%s, %s)
            """, [id_konten, g])

        return redirect('biru:podcaster')

    else:
        # Render form untuk update podcast
        return render(request, 'create_podcast.html')

    
def podcaster(request):
    # Fetch podcaster's podcast details from the database
    email = request.session.get('user_email', None)
    curr.execute("""
        SELECT 
            k.id AS id_konten,
            a.nama AS nama_podcaster,
            k.judul AS judul_podcast, 
            COUNT(e.id_episode) AS jumlah_episode, 
            SUM(k.durasi) AS total_durasi 
        FROM 
            marmut.podcast p 
        LEFT JOIN 
            marmut.episode e ON p.id_konten = e.id_konten_podcast 
        LEFT JOIN 
            marmut.konten k ON p.id_konten = k.id
        LEFT JOIN 
            marmut.akun a ON p.email_podcaster = a.email
        WHERE 
            p.email_podcaster = %s 
        GROUP BY 
            k.id, a.nama, k.judul, p.id_konten
    """, [email])
    podcasts = curr.fetchall()

    podcasts = [(id_konten, nama_podcaster, judul_podcast, jumlah_episode, format_durasi_dua(total_durasi)) for id_konten, nama_podcaster, judul_podcast, jumlah_episode, total_durasi in podcasts]

    # Prepare context data for rendering
    context = {
        'nama_podcaster' : podcasts[0],
        'podcasts': podcasts,
    }

    if not podcasts:
        context['message'] = 'Kamu belum memiliki podcast.'

    return render(request, 'create_podcast.html', context)

# chart list
def get_chart_details(request):
    chart_types = []
    chart_details = {}

    # Fetch chart types
    curr.execute("SELECT DISTINCT tipe FROM marmut.Chart")
    chart_types_raw = curr.fetchall()
    
    # Convert raw chart types into a list
    chart_types = [chart_type[0] for chart_type in chart_types_raw]
    
    # Fetch chart details for each chart type
    for chart_type in chart_types:
        curr.execute("""
            SELECT C.tipe, K.judul AS title, A.id AS artist_id, AK.nama AS artist_name, AK.email AS artist_email, K.tanggal_rilis AS release_date, S.total_play AS plays
            FROM marmut.CHART C
            JOIN marmut.PLAYLIST_SONG PS ON C.id_playlist = PS.id_playlist
            JOIN marmut.SONG S ON PS.id_song = S.id_konten
            JOIN marmut.KONTEN K ON S.id_konten = K.id
            JOIN marmut.ARTIST A ON S.id_artist = A.id
            JOIN marmut.AKUN AK ON A.email_akun = AK.email
            WHERE C.tipe = %s
            ORDER BY S.total_play DESC
            LIMIT 20
        """, [chart_type])
        # Fetch all rows
        rows = curr.fetchall()
        
        # Create a list of dictionaries for each row
        chart_details[chart_type] = [{'tipe': row[0], 'title': row[1], 'artist_id': row[2], 'artist_name': row[3], 'artist_email': row[4], 'release_date': row[5], 'plays': row[6]} for row in rows]

    # Render the chart template with chart types and details
    return render(request, 'chart_list.html', {'chart_types': chart_types, 'chart_details': chart_details})