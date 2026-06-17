from django.shortcuts import render, redirect
from django.db import connection

def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok
            FROM buku_buku WHERE status_buku = 'Aktif' ORDER BY id
        """)
        buku = cursor.fetchall()
    return render(request, 'buku/list.html', {'buku': buku})

def buku_tambah(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO buku_buku
                (judul, pengarang, kategori, penerbit, tahun_terbit, isbn, rak, stok, deskripsi, status_buku)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                request.POST.get('judul', ''),
                request.POST.get('pengarang', ''),
                request.POST.get('kategori', ''),
                request.POST.get('penerbit', ''),
                request.POST.get('tahun_terbit', 0),
                request.POST.get('isbn', ''),
                request.POST.get('rak', ''),
                request.POST.get('stok', 0),
                request.POST.get('deskripsi', ''),
                'Aktif'
            ])
        return redirect('/buku/')
    return render(request, 'buku/tambah.html')

def edit_buku(request, id):
    with connection.cursor() as cursor:
        if request.method == "POST":
            cursor.execute("""
                UPDATE buku_buku
                SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, isbn=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id=%s
            """, [
                request.POST.get('judul', ''),
                request.POST.get('pengarang', ''),
                request.POST.get('kategori', ''),
                request.POST.get('penerbit', ''),
                request.POST.get('tahun_terbit', 0),
                request.POST.get('isbn', ''),
                request.POST.get('rak', ''),
                request.POST.get('stok', 0),
                request.POST.get('deskripsi', ''),
                id
            ])
            return redirect('/buku/')
        
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, isbn, rak, stok, deskripsi
            FROM buku_buku WHERE id=%s
        """, [id])
        row = cursor.fetchone()

    buku = {"id": row[0], "judul": row[1], "pengarang": row[2], "kategori": row[3], "penerbit": row[4],
            "tahun_terbit": row[5], "isbn": row[6], "rak": row[7], "stok": row[8], "deskripsi": row[9]}
    return render(request, 'buku/edit.html', {'buku': buku})

def delete_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE buku_buku SET status_buku='Tidak Aktif' WHERE id=%s", [id])
    return redirect('/buku/')

def detail_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, isbn, rak, stok, deskripsi
            FROM buku_buku WHERE id=%s
        """, [id])
        row = cursor.fetchone()

    buku = {"id": row[0], "judul": row[1], "pengarang": row[2], "kategori": row[3], "penerbit": row[4],
            "tahun_terbit": row[5], "isbn": row[6], "rak": row[7], "stok": row[8], "deskripsi": row[9]}
    return render(request, 'buku/detail.html', {'buku': buku})
