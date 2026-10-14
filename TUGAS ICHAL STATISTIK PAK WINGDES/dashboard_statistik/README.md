# Dashboard Statistik — Flask

## Isi
- `/` : dashboard statistik deskriptif data latihan 10 kelompok x 10 orang dari Excel, dengan tautan langsung ke halaman Data Uji.
- `/data-uji` : analisis deskriptif 30 observasi dari `data_uji(1).pdf`, regresi Persepsi (X) → PD (Y), prediksi, grafik, dan ekspor CSV.

## Menjalankan di Windows / VS Code
1. Ekstrak folder ZIP dan buka folder `dashboard_statistik` di VS Code.
2. Buat virtual environment: `py -m venv .venv`
3. Aktifkan PowerShell: `.venv\Scripts\Activate.ps1`
4. Pasang dependensi: `python -m pip install -r requirements.txt`
5. Jalankan: `python app.py`
6. Buka `http://127.0.0.1:5000` atau `http://127.0.0.1:5000/data-uji`.

Jika PowerShell menolak aktivasi, jalankan langsung `.venv\Scripts\python.exe -m pip install -r requirements.txt`, lalu `.venv\Scripts\python.exe app.py`.

## Catatan
- Chart.js dan font Inter dimuat dari CDN sehingga koneksi internet diperlukan untuk aset tersebut.
- Untuk deployment publik, jangan gunakan `debug=True`; gunakan server WSGI seperti Gunicorn pada host yang mendukung Python. Netlify terutama untuk frontend statis/serverless dan tidak menjalankan Flask server konvensional sebagai proses web permanen.
- Data uji diketik sesuai 30 baris PDF; verifikasi kembali unit/definisi kolom, khususnya `jam`, `Persepsi`, dan `PD`.
