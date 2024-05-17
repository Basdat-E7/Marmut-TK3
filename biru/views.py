from django.shortcuts import render
from django.db import OperationalError, ProgrammingError, connection
from django.http import HttpResponseNotFound
from utils.query import *

def format_durasi(menit):
    jam = menit // 60
    sisa_menit = menit % 60
    return f'{jam} jam {sisa_menit} menit' if jam > 0 else f'{sisa_menit} menit'

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

#def get_chart_details(request):
#    # Fetch chart types
#    curr.execute("SELECT DISTINCT tipe FROM marmut.Chart")
#    chart_types = curr.fetchall()
#    print("Chart Types:", chart_types) 
#
#    # Fetch chart details
#    chart_details = {}
#    for chart_type in chart_types:
#        curr.execute("""
#            SELECT C.tipe, K.judul AS title, A.id AS artist, K.tanggal_rilis AS release_date, S.total_play AS plays
#            FROM marmut.CHART C
#            JOIN marmut.PLAYLIST_SONG PS ON C.id_playlist = PS.id_playlist
#            JOIN marmut.SONG S ON PS.id_song = S.id_konten
#            JOIN marmut.KONTEN K ON S.id_konten = K.id
#            JOIN marmut.ARTIST A ON S.id_artist = A.id
#            WHERE C.tipe = %s
#            ORDER BY S.total_play DESC
#            LIMIT 20
#        """, [chart_type[0]])
#        chart_details[chart_type[0]] = curr.fetchall()
#
#    print("Chart Details:", chart_details) 
#
#    return render(request, 'chart_list.html', {'chart_details': chart_details, 'chart_types': chart_types})#

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