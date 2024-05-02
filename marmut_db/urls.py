from django.urls import path
from marmut_db.views import show_main
from . import views

app_name = 'marmut_db'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/label/', views.register_label, name='register_label'),
]