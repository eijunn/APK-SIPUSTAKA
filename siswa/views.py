from django.shortcuts import render, redirect
from django.db import connection, DatabaseError

def siswa_list(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nama, kelas, nis, is_active FROM siswa_siswa ORDER BY id
            """)
            rows = cursor.fetchall()
    except DatabaseError:
        rows = []
    return render(request, 'siswa/list.html', {'siswa': rows})

def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa_siswa WHERE id=%s", [id])
        data = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM peminjaman_peminjaman WHERE siswa_id=%s", [id])
        total_pinjam = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM peminjaman_peminjaman WHERE siswa_id=%s AND status='Dipinjam'", [id])
        aktif = cursor.fetchone()[0]

    siswa = {'id': data[0], 'nama': data[1], 'kelas': data[2], 'nis': data[3], 'is_active': data[4]}
    return render(request, 'siswa/detail.html', {'siswa': siswa, 'total_pinjam': total_pinjam, 'peminjaman_aktif': f'{aktif} buku masih dipinjam.'})

def siswa_tambah(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO siswa_siswa (nama, kelas, nis, is_active) VALUES (%s, %s, %s, %s)",
                          [request.POST['nama'], request.POST.get('kelas', ''), request.POST.get('nis', ''), True])
        return redirect('/siswa/')
    return render(request, 'siswa/tambah.html')

def siswa_edit(request, id):
    with connection.cursor() as cursor:
        if request.method == "POST":
            cursor.execute("UPDATE siswa_siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s WHERE id=%s",
                          [request.POST['nama'], request.POST.get('kelas', ''), request.POST.get('nis', ''), True, id])
            return redirect('/siswa/')
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa_siswa WHERE id=%s", [id])
        data = cursor.fetchone()

    siswa = {'id': data[0], 'nama': data[1], 'kelas': data[2], 'nis': data[3], 'is_active': data[4]}
    return render(request, 'siswa/edit.html', {'siswa': siswa})

def siswa_hapus(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM siswa_siswa WHERE id=%s", [id])
    return redirect('/siswa/')