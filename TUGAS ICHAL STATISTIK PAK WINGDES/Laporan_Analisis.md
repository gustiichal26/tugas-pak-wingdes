# Laporan Analisis Statistik Deskriptif dan Regresi

## Sumber dan batasan
Data uji ditranskripsikan dari `data_uji(1).pdf`, terdiri dari 30 observasi dengan variabel jam, tinggi, berat, Persepsi, dan PD. PDF tidak menjelaskan satuan/definisi lengkap variabel, sehingga interpretasi kontekstual dibatasi. Statistik SD dan varians di bawah memakai rumus sampel (n−1). Kuartil memakai interpolasi linear (posisi (n−1)p).

## Statistik deskriptif data uji
| Variabel | n | Mean | Median | Modus | Min | Maks | Rentang | Q1 | Q3 | IQR | SD sampel |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| jam | 30 | 5.2333 | 6 | 7 | 1 | 8 | 7 | 4.25 | 7 | 2.75 | 2.2234 |
| tinggi | 30 | 167.0333 | 168 | 170 | 151 | 184 | 33 | 162.5 | 170 | 7.5 | 7.8190 |
| berat | 30 | 63.2000 | 58 | 60 | 45 | 140 | 95 | 50.5 | 62.25 | 11.75 | 21.6610 |
| Persepsi | 30 | 6.5667 | 6.5 | 9 | 2 | 9 | 7 | 5 | 8 | 3 | 1.9061 |
| PD | 30 | 7.0000 | 7.5 | 9 | 3 | 9 | 6 | 5 | 9 | 4 | 2.0172 |

## Insight dan keputusan yang disarankan
1. Rata-rata Persepsi 6.5667 dan PD 7.0000; median masing-masing 6.5 dan 7.5. Modus kedua variabel adalah 9. Kategorisasi baik/buruk hanya boleh dibuat jika definisi skala diberikan.
2. Korelasi Persepsi–PD adalah positif sedang (r=0.4933). Ini asosiasi, bukan bukti kausalitas.
3. Berat mempunyai mean 63.2 dan median 58, dengan nilai maksimum 140. Dengan metode IQR, Q1=50.5, Q3=62.25, IQR=11.75 dan pagar atas 79.875; berat 80, 81, 130, dan 140 berada di atas pagar. Periksa nilai sumber dan satuan, jangan otomatis menghapusnya.
4. Tinggi mempunyai mean 167.03 dan median 168; ringkasan pusat berdekatan, namun sebaran tetap perlu dilihat bersama SD 7.819.
5. Sebelum keputusan praktis, konfirmasi arti `jam`, satuan tinggi/berat, cara pengukuran, dan arti skala Persepsi/PD.

## Regresi linear sederhana
Variabel bebas X = Persepsi; variabel terikat Y = PD. Estimasi kuadrat terkecil dari 30 observasi menghasilkan:

**PD_hat = 3.572287 + 0.521987 × Persepsi**

- Intersep a = 3.572287
- Slope b = 0.521987
- Korelasi Pearson r = 0.493253
- Koefisien determinasi R² = 0.243299 (24.33%)
- RMSE in-sample = 1.7252

Interpretasi: kenaikan 1 poin Persepsi berkaitan dengan kenaikan prediksi PD sekitar 0.522 poin. R² 24.33% menunjukkan model hanya menjelaskan sebagian variasi PD; faktor lain dan variasi acak masih berperan. Jangan menafsirkan slope sebagai sebab-akibat.

## Contoh prediksi
| Persepsi (X) | Prediksi PD (Ŷ) |
|---:|---:|
| 5 | 6.1822 |
| 6 | 6.7042 |
| 7 | 7.2262 |
| 8 | 7.7482 |
| 9 | 8.2702 |

Nilai prediksi adalah nilai rata-rata model dan dapat berupa desimal meski PD tercatat sebagai bilangan bulat. Model dilatih dan dievaluasi pada data yang sama; kinerja prediksi di data baru belum diketahui. Untuk bagian 3B, masukkan data minggu depan, hitung statistiknya kembali, lalu evaluasi prediksi dengan MAE/RMSE pada data baru.

## Keputusan praktis
- Audit terlebih dahulu empat nilai berat di atas pagar IQR, khususnya 130 dan 140, terhadap formulir asli.
- Laporkan hubungan Persepsi–PD sebagai hubungan positif sedang, bukan hubungan kausal.
- Jangan mengandalkan Persepsi saja untuk memprediksi PD karena R² relatif terbatas.
- Kumpulkan data baru dengan definisi variabel dan unit yang jelas; gunakan data baru untuk validasi model.
