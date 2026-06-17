from django.urls import path
from . import views

urlpatterns = [
    path('', views.buku_list, name='buku_list'),
    path('tambah/', views.buku_tambah, name='buku_tambah'),
    path('edit/<int:id>/', views.edit_buku, name='edit_buku'),
    path('detail/<int:id>/', views.detail_buku, name='detail_buku'),
    path('hapus/<int:id>/', views.delete_buku, name='delete_buku'),
]