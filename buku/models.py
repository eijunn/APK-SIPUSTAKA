from django.db import models


class Buku(models.Model):
	judul = models.CharField(max_length=255)
	pengarang = models.CharField(max_length=255, blank=True, null=True)
	kategori = models.CharField(max_length=100, blank=True, null=True)
	penerbit = models.CharField(max_length=255, blank=True, null=True)
	tahun_terbit = models.IntegerField(blank=True, null=True)
	isbn = models.CharField(max_length=20, blank=True, null=True)
	rak = models.CharField(max_length=50, blank=True, null=True)
	stok = models.IntegerField(default=0)
	deskripsi = models.TextField(blank=True, null=True)
	status_buku = models.CharField(max_length=50, default='Aktif')

	def __str__(self):
		return self.judul
