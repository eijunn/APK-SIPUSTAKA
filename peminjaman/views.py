from django.shortcuts import render, redirect
from django.db import connection

def peminjaman_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama, b.judul, p.tanggal_pinjam, p.jatuh_tempo, p.keperluan, p.status
            FROM peminjaman_peminjaman p
            JOIN siswa_siswa s ON p.siswa_id = s.id
            JOIN buku_buku b ON p.buku_id = b.id
            ORDER BY p.id
        """)
        data = cursor.fetchall()

    return render(request, 'peminjaman/list.html', {'data': data})

def peminjaman_tambah(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, nis FROM siswa_siswa ORDER BY nama")
        siswa = cursor.fetchall()
        cursor.execute("SELECT id, judul, stok FROM buku_buku WHERE stok > 0 AND status_buku = 'Aktif' ORDER BY judul")
        buku = cursor.fetchall()

        if request.method == "POST":
            siswa_id = request.POST.get("siswa")
            buku_id = request.POST.get("buku")
            tanggal_pinjam = request.POST.get("tanggal_pinjam")
            jatuh_tempo = request.POST.get("jatuh_tempo")
            keperluan = request.POST.get("keperluan")

            cursor.execute("""
                INSERT INTO peminjaman_peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, 'Dipinjam'])

            cursor.execute("UPDATE buku_buku SET stok = stok - 1 WHERE id = %s", [buku_id])
            return redirect('/peminjaman/')

    return render(request, 'peminjaman/tambah.html', {'siswa': siswa, 'buku': buku})

def kembalikan_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT buku_id FROM peminjaman_peminjaman WHERE id=%s", [id])
        row = cursor.fetchone()

        if row:
            buku_id = row[0]
            cursor.execute("UPDATE peminjaman_peminjaman SET status='Dikembalikan' WHERE id=%s", [id])
            cursor.execute("UPDATE buku_buku SET stok = stok + 1 WHERE id=%s", [buku_id])

    return redirect('/peminjaman/')

def peminjaman_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama, b.judul, p.tanggal_pinjam, p.jatuh_tempo, p.keperluan, p.status
            FROM peminjaman_peminjaman p
            JOIN siswa_siswa s ON p.siswa_id = s.id
            JOIN buku_buku b ON p.buku_id = b.id
            WHERE p.id = %s
        """, [id])
        row = cursor.fetchone()

    if row:
        peminjaman = {"id": row[0], "nama": row[1], "judul": row[2], "tanggal_pinjam": row[3],
                      "jatuh_tempo": row[4], "keperluan": row[5], "status": row[6]}
        return render(request, 'peminjaman/detail.html', {'peminjaman': peminjaman})
    return redirect('/peminjaman/')