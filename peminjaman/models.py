from django.db import models
from siswa.models import Siswa
from buku.models import Buku


class Peminjaman(models.Model):
	siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
	buku = models.ForeignKey(Buku, on_delete=models.CASCADE, null=True, blank=True)
	tanggal_pinjam = models.DateField(auto_now_add=True)
	jatuh_tempo = models.DateField(blank=True, null=True)
	keperluan = models.CharField(max_length=100, blank=True, null=True)
	status = models.CharField(max_length=50, default='Dipinjam')

	def __str__(self):
		return f"{self.siswa} - {self.status}"
