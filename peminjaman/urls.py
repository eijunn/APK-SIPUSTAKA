from django.urls import path
from . import views

urlpatterns = [

    path('', views.peminjaman_list, name='peminjaman_list'),
     path('tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
      path(
        'kembalikan/<int:id>/',
        views.kembalikan_buku,
        name='kembalikan_buku'
    ),
    

]