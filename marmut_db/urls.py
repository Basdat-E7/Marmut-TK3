from django.urls import path
from marmut_db.views import show_main
from . import views

app_name = 'marmut_db'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/label/', views.register_label, name='register_label'),
    path('langganan_paket/', views.langganan_paket_page, name='langganan_paket'),
    path('langganan_paket/submit/', views.langganan_paket_submit, name='langganan_paket_submit'),
    path('langganan_paket/submit/confirm', views.langganan_paket, name='langganan_paket_confirm'),
    path('langganan_paket/purchase_history', views.purchase_history, name='purchase_history'),
    path('downloaded_songs/', views.downloaded_songs, name='downloaded_songs'),
    path('search/', views.search, name='search'),
]