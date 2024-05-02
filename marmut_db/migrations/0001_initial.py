# Generated by Django 5.0.4 on 2024-05-02 01:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Akun',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('nama', models.CharField(max_length=100)),
                ('gender', models.IntegerField()),
                ('tempat_lahir', models.CharField(max_length=50)),
                ('tanggal_lahir', models.DateField()),
                ('is_verified', models.BooleanField()),
                ('kota_asal', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Konten',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('judul', models.CharField(max_length=100)),
                ('tanggal_rilis', models.DateField()),
                ('tahun', models.IntegerField()),
                ('durasi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('kontak', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paket',
            fields=[
                ('jenis', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('harga', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PemilikHakCipta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rate_royalti', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=50)),
                ('id_konten', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.konten')),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('judul', models.CharField(max_length=100)),
                ('jumlah_lagu', models.IntegerField(default=0)),
                ('total_durasi', models.IntegerField(default=0)),
                ('id_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.label')),
            ],
        ),
        migrations.CreateModel(
            name='NonPremium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='id_pemilik_hak_cipta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.pemilikhakcipta'),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email_akun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('id_pemilik_hak_cipta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.pemilikhakcipta')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('tipe', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('id_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.playlist')),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_konten', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.konten')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id_episode', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('judul', models.CharField(max_length=100)),
                ('deskripsi', models.CharField(max_length=500)),
                ('durasi', models.IntegerField()),
                ('tanggal_rilis', models.DateField()),
                ('id_konten_podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.podcast')),
            ],
        ),
        migrations.CreateModel(
            name='Podcaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
            ],
        ),
        migrations.AddField(
            model_name='podcast',
            name='email_podcaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.podcaster'),
        ),
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_play', models.IntegerField(default=0)),
                ('total_download', models.IntegerField(default=0)),
                ('id_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.album')),
                ('id_artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.artist')),
                ('id_konten', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.konten')),
            ],
        ),
        migrations.CreateModel(
            name='Royalti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.IntegerField()),
                ('id_pemilik_hak_cipta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.pemilikhakcipta')),
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.song')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.playlist')),
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.song')),
            ],
        ),
        migrations.CreateModel(
            name='DownloadedSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_downloader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.premium')),
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.song')),
            ],
        ),
        migrations.CreateModel(
            name='AkunPlaySong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu', models.DateTimeField()),
                ('email_pemain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.song')),
            ],
        ),
        migrations.CreateModel(
            name='Songwriter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email_akun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('id_pemilik_hak_cipta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.pemilikhakcipta')),
            ],
        ),
        migrations.CreateModel(
            name='SongwriterWriteSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.song')),
                ('id_songwriter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.songwriter')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp_dimulai', models.DateTimeField()),
                ('timestamp_berakhir', models.DateTimeField()),
                ('metode_bayar', models.CharField(max_length=50)),
                ('nominal', models.IntegerField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('jenis_paket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.paket')),
            ],
        ),
        migrations.CreateModel(
            name='UserPlaylist',
            fields=[
                ('id_user_playlist', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('judul', models.CharField(max_length=100)),
                ('deskripsi', models.CharField(max_length=500)),
                ('jumlah_lagu', models.IntegerField()),
                ('tanggal_dibuat', models.DateField()),
                ('total_durasi', models.IntegerField(default=0)),
                ('email_pembuat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('id_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.playlist')),
            ],
        ),
        migrations.CreateModel(
            name='AkunPlayUserPlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu', models.DateTimeField()),
                ('email_pemain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marmut_db.akun')),
                ('email_pembuat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists_made', to='marmut_db.userplaylist')),
                ('id_user_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_users', to='marmut_db.userplaylist')),
            ],
        ),
    ]
