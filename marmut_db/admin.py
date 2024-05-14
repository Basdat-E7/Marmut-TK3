from django.contrib import admin
from .models import Akun, Podcaster, Artist, Songwriter

# Register your models here.
admin.site.register(Akun)
admin.site.register(Podcaster)
admin.site.register(Artist)
admin.site.register(Songwriter)