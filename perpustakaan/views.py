from django.shortcuts import render
from django.db import connection, DatabaseError

def dashboard(request):

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COALESCE(SUM(stok),0)
                FROM buku_buku
                WHERE status_buku='Aktif'
            """)
            total_buku = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM buku_buku
                WHERE status_buku='Aktif'
            """)
            total_judul = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM peminjaman_peminjaman
                WHERE status='Dipinjam'
            """)
            dipinjam = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM peminjaman_peminjaman
                WHERE status='Dikembalikan'
            """)
            dikembalikan = cursor.fetchone()[0]

            cursor.execute("""
                SELECT
                    judul,
                    stok
                FROM buku_buku
                WHERE status_buku='Aktif'
                ORDER BY stok DESC
                LIMIT 5
            """)
            stok_raw = cursor.fetchall()
    except DatabaseError as e:
        # Jika tabel belum dibuat atau DB tidak tersedia, jangan crash
        print("Database error in dashboard view:", e)
        total_buku = 0
        total_judul = 0
        dipinjam = 0
        dikembalikan = 0
        stok_raw = []

    stok_buku = []

    for judul, stok in stok_raw:

        persen = min(stok * 10, 100)

        stok_buku.append(
            (
                judul,
                stok,
                persen
            )
        )

    # Hitung persentase untuk ringkasan (untuk progress bars)
    if total_buku and total_buku > 0:
        dipinjam_percent = min(round(dipinjam / total_buku * 100), 100)
        dikembalikan_percent = min(round(dikembalikan / total_buku * 100), 100)
    else:
        dipinjam_percent = 0
        dikembalikan_percent = 0

    return render(
        request,
        'dashboard.html',
        {
            'total_buku': total_buku,
            'total_judul': total_judul,
            'dipinjam': dipinjam,
            'dikembalikan': dikembalikan,
            'dipinjam_percent': dipinjam_percent,
            'dikembalikan_percent': dikembalikan_percent,
            'stok_buku': stok_buku,
        }
    )