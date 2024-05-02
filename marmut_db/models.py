from django.db import models
from uuid import uuid4

class Akun(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
    gender = models.IntegerField()
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField()
    kota_asal = models.CharField(max_length=50)

class Paket(models.Model):
    jenis = models.CharField(max_length=50, primary_key=True)
    harga = models.IntegerField()

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    jenis_paket = models.ForeignKey(Paket, on_delete=models.CASCADE)
    email = models.ForeignKey(Akun, on_delete=models.CASCADE)
    timestamp_dimulai = models.DateTimeField()
    timestamp_berakhir = models.DateTimeField()
    metode_bayar = models.CharField(max_length=50)
    nominal = models.IntegerField()

class Premium(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE)

class NonPremium(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE)

class Konten(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    tanggal_rilis = models.DateField()
    tahun = models.IntegerField()
    durasi = models.IntegerField()

class Genre(models.Model):
    id_konten = models.ForeignKey(Konten, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)

class Podcaster(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE)

class Podcast(models.Model):
    id_konten = models.OneToOneField(Konten, on_delete=models.CASCADE)
    email_podcaster = models.ForeignKey(Podcaster, on_delete=models.CASCADE)

class Episode(models.Model):
    id_episode = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_konten_podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    durasi = models.IntegerField()
    tanggal_rilis = models.DateField()

class PemilikHakCipta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    rate_royalti = models.IntegerField()

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email_akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Songwriter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email_akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Label(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    kontak = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField(default=0)
    id_label = models.ForeignKey(Label, on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0)

class Song(models.Model):
    id_konten = models.OneToOneField(Konten, on_delete=models.CASCADE)
    id_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    id_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    total_play = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)

class SongwriterWriteSong(models.Model):
    id_songwriter = models.ForeignKey(Songwriter, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)

class DownloadedSong(models.Model):
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    email_downloader = models.ForeignKey(Premium, on_delete=models.CASCADE)

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class Chart(models.Model):
    tipe = models.CharField(max_length=50, primary_key=True)
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

class UserPlaylist(models.Model):
    email_pembuat = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_user_playlist = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    jumlah_lagu = models.IntegerField()
    tanggal_dibuat = models.DateField()
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0)

class Royalti(models.Model):
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    jumlah = models.IntegerField()

class AkunPlayUserPlaylist(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_user_playlist = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE, related_name='playlist_users')
    email_pembuat = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE, related_name='playlists_made')
    waktu = models.DateTimeField()

class AkunPlaySong(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    waktu = models.DateTimeField()

class PlaylistSong(models.Model):
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)