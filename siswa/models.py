from django.db import models


class Siswa(models.Model):
	nama = models.CharField(max_length=200)
	kelas = models.CharField(max_length=50, blank=True, null=True)
	nis = models.CharField(max_length=50, blank=True, null=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.nama
