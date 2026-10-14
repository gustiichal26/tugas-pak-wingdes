# Tugas Statistik Ichal — Paket Gabungan

Paket ini menggabungkan dashboard statistik data latihan dan analisis `data_uji`.

## Cara menjalankan dashboard
1. Ekstrak ZIP.
2. Buka folder `dashboard_statistik` di VS Code.
3. Di terminal VS Code, jalankan `python -m pip install -r requirements.txt`.
4. Jalankan `python app.py`.
5. Buka halaman berikut di browser:
   - `http://127.0.0.1:5000/` — dashboard data latihan (10 kelompok x 10 orang).
   - `http://127.0.0.1:5000/data-uji` — data uji 30 observasi, statistik deskriptif, grafik, regresi linear, dan prediksi.

## File tambahan
- `data_uji_sumber.pdf` — PDF sumber data uji.
- `Data_Uji_dan_Analisis.xlsx` — data mentah, statistik deskriptif, koefisien regresi, dan prediksi.
- `Laporan_Analisis_Statistik.docx` serta `Laporan_Analisis.md` — laporan analisis.

Catatan: arti/satuan kolom `jam`, `Persepsi`, dan `PD` tidak dijelaskan lengkap di PDF sumber. Konfirmasi definisinya sebelum menarik kesimpulan substantif. Nilai berat yang tinggi ditandai untuk pemeriksaan, bukan otomatis dihapus.
