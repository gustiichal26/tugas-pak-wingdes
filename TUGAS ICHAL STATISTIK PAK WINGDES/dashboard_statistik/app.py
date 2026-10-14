from flask import Flask, render_template, jsonify
import math
import statistics
from collections import Counter

app = Flask(__name__)

# =============================================
# DATA MENTAH — 10 KELOMPOK x 10 ORANG
# Sumber: tugas_statistika_deskriptif.xlsx
# =============================================
RAW_DATA = {
    "Kelompok 1":  [5, 4, 3, 2, 1, 2, 8, 1, 5, 1],
    "Kelompok 2":  [5, 5, 4, 3, 2, 2, 8, 1, 5, 5],
    "Kelompok 3":  [5, 5, 5, 4, 3, 3, 8, 1, 5, 5],
    "Kelompok 4":  [5, 5, 5, 5, 4, 3, 9, 2, 5, 5],
    "Kelompok 5":  [6, 6, 5, 5, 5, 4, 9, 2, 5, 5],
    "Kelompok 6":  [6, 6, 6, 6, 6, 7, 9, 2, 5, 5],
    "Kelompok 7":  [6, 6, 6, 7, 7, 8, 10, 3, 5, 5],
    "Kelompok 8":  [6, 6, 6, 8, 8, 8, 10, 3, 5, 5],
    "Kelompok 9":  [5, 5, 7, 9, 9, 9, 10, 3, 8, 5],
    "Kelompok 10": [6, 7, 8, 6, 10, 9, 9, 4, 10, 5],
}

ORANG_LABELS = ["Orang 1","Orang 2","Orang 3","Orang 4","Orang 5","Orang 6","Orang 7","Orang 8","Orang 9","Orang 10"]


def hitung_statistik(data):
    n = len(data)
    sorted_d = sorted(data)
    mean = sum(data) / n
    if n % 2 == 0:
        median = (sorted_d[n//2-1] + sorted_d[n//2]) / 2
    else:
        median = sorted_d[n//2]
    freq = Counter(data)
    max_freq = max(freq.values())
    modes = [k for k, v in freq.items() if v == max_freq]
    modus = modes[0]
    minimum = min(data)
    maksimum = max(data)
    rentang = maksimum - minimum

    def quartile(sd, q):
        idx = q / 4 * (len(sd) - 1)
        lower = int(idx)
        upper = lower + 1
        if upper >= len(sd):
            return sd[-1]
        return sd[lower] + (idx - lower) * (sd[upper] - sd[lower])

    q1 = quartile(sorted_d, 1)
    q3 = quartile(sorted_d, 3)
    iqr = q3 - q1
    varians_sampel = sum((x - mean)**2 for x in data) / (n - 1)
    sd_sampel = math.sqrt(varians_sampel)
    varians_populasi = sum((x - mean)**2 for x in data) / n
    sd_populasi = math.sqrt(varians_populasi)
    selisih_sd = sd_sampel - sd_populasi
    cv = (sd_sampel / mean) * 100 if mean != 0 else 0
    return {
        "n": n, "mean": round(mean, 4), "median": round(median, 4), "modus": modus,
        "min": minimum, "maks": maksimum, "range": rentang,
        "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(iqr, 4),
        "varians_sampel": round(varians_sampel, 4), "sd_sampel": round(sd_sampel, 4),
        "sd_populasi": round(sd_populasi, 4), "selisih_sd": round(selisih_sd, 4),
        "cv": round(cv, 4),
    }


def build_all_stats():
    all_stats = {}
    for k, d in RAW_DATA.items():
        all_stats[k] = hitung_statistik(d)
    avg_sd = sum(s["sd_sampel"] for s in all_stats.values()) / len(all_stats)
    sd_sorted = sorted(all_stats.items(), key=lambda x: x[1]["sd_sampel"], reverse=True)
    rank_map = {k: i+1 for i, (k, _) in enumerate(sd_sorted)}
    for k, v in all_stats.items():
        sd = v["sd_sampel"]
        if sd > 1.1 * avg_sd:
            v["kategori"] = "Sebaran lebar (heterogen)"
        elif sd < 0.9 * avg_sd:
            v["kategori"] = "Sebaran sempit (homogen)"
        else:
            v["kategori"] = "Sebaran sedang"
        v["peringkat_sd"] = rank_map[k]
    all_values = [val for d in RAW_DATA.values() for val in d]
    gabungan = hitung_statistik(all_values)
    gabungan["kategori"] = "Seluruh data"
    gabungan["peringkat_sd"] = "-"
    all_stats["Gabungan (100 orang)"] = gabungan
    return all_stats, avg_sd


ALL_STATS, AVG_SD = build_all_stats()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    knames = list(RAW_DATA.keys())
    sd_list = [ALL_STATS[k]["sd_sampel"] for k in knames]
    mean_list = [ALL_STATS[k]["mean"] for k in knames]
    cv_list = [ALL_STATS[k]["cv"] for k in knames]
    median_list = [ALL_STATS[k]["median"] for k in knames]
    min_list = [ALL_STATS[k]["min"] for k in knames]
    maks_list = [ALL_STATS[k]["maks"] for k in knames]
    range_list = [ALL_STATS[k]["range"] for k in knames]
    q1_list = [ALL_STATS[k]["q1"] for k in knames]
    q3_list = [ALL_STATS[k]["q3"] for k in knames]
    iqr_list = [ALL_STATS[k]["iqr"] for k in knames]

    keputusan = [
        "Kelompok 10 memiliki rata-rata tertinggi (7.40) dan Kelompok 1 terendah (3.20). Terdapat kesenjangan 4.2 poin yang perlu menjadi perhatian dalam pemerataan hasil belajar.",
        "Kelompok 5 dan 6 memiliki SD sampel terkecil (1.7512), sehingga skor dalam dua kelompok ini paling rapat dibanding kelompok lain. Ini tidak otomatis membuktikan penyebab atau kualitas proses pembelajaran.",
        "Kelompok 9 memiliki SD terbesar (2.3570) → nilai sangat heterogen. Perlu intervensi individual karena ada kesenjangan besar antar anggota kelompok.",
        "Koefisien Variasi (CV) tertinggi pada Kelompok 1 (71.87%) menunjukkan variasi relatif terbesar terhadap mean-nya, meskipun mean-nya rendah.",
        "2 dari 10 kelompok dikategorikan 'sebaran lebar (heterogen)' yaitu Kelompok 1 dan Kelompok 9, sementara 80% kelompok lainnya memiliki sebaran sedang atau sempit.",
        "Rata-rata gabungan 100 orang = 5.46 dengan SD = 2.3112. Nilai ini menunjukkan distribusi data yang cukup bervariasi secara keseluruhan.",
        "SD sampel selalu lebih besar dari SD populasi (menggunakan pembagi n-1 vs n). Perbedaan ini wajar dan semakin kecil seiring bertambahnya ukuran sampel.",
        "Range semua kelompok berkisar 6-7, kecuali Kelompok 10 (range=6). Artinya penyebaran nilai dari minimum ke maksimum relatif seragam antar kelompok.",
        "Median dan mean yang berdekatan pada sebagian besar kelompok menunjukkan distribusi yang mendekati simetris, tidak terlalu condong ke kiri maupun kanan.",
        "Rata-rata meningkat dari kelompok awal ke kelompok akhir pada data ini. Karena nomor kelompok bukan variabel penyebab yang terdefinisi, pola ini perlu diperlakukan sebagai deskripsi, bukan bukti sebab-akibat."
    ]

    stats_per_kelompok = {}
    for k in knames:
        stats_per_kelompok[k] = ALL_STATS[k]

    return jsonify({
        "kelompok": knames,
        "mean": mean_list,
        "sd_sampel": sd_list,
        "cv": cv_list,
        "median": median_list,
        "min": min_list,
        "maks": maks_list,
        "range": range_list,
        "q1": q1_list,
        "q3": q3_list,
        "iqr": iqr_list,
        "orang_labels": ORANG_LABELS,
        "raw_data": {k: list(v) for k, v in RAW_DATA.items()},
        "keputusan": keputusan,
        "avg_sd_all": round(AVG_SD, 4),
        "gabungan": ALL_STATS["Gabungan (100 orang)"],
        "stats_per_kelompok": stats_per_kelompok,
    })



# DATA UJI dari data_uji(1).pdf: 30 observasi.
# Kolom mengikuti sumber; arti unit/definisi jam tidak diasumsikan.
DATA_UJI = [
[5,169,81,4,4],[5,170,49,2,9],[6,170,56,5,8],[8,162,50,8,7],[7,166,50,6,9],
[7,160,79,6,7],[5,180,80,6,4],[7,151,48,7,6],[5,170,130,6,8],[8,180,56,3,5],
[7,158,52,7,8],[7,157,59,6,6],[6,174,64,9,9],[6,168,49,5,8],[6,167,50,8,9],
[2,173,63,5,4],[7,165,58,9,9],[1,170,60,9,9],[4,160,57,9,9],[5,152,60,5,3],
[6,167,52,6,5],[3,167,58,9,9],[1,170,60,9,9],[6,164,57,8,4],[7,155,45,7,7],
[8,168,45,5,5],[2,170,60,5,5],[1,174,68,9,9],[7,170,60,7,7],[2,184,140,7,9]
]
DATA_COLUMNS = ["jam", "tinggi", "berat", "Persepsi", "PD"]

def data_uji_analisis():
    cols = {c: [row[i] for row in DATA_UJI] for i, c in enumerate(DATA_COLUMNS)}
    summary = {}
    for c, values in cols.items():
        s = sorted(values); n = len(s); mean = sum(s)/n
        def quantile(p):
            pos = (n-1)*p; lo = int(pos); hi = min(lo+1,n-1)
            return s[lo] + (pos-lo)*(s[hi]-s[lo])
        freq = {v: values.count(v) for v in set(values)}
        maxfreq = max(freq.values())
        modes = sorted([v for v, f in freq.items() if f == maxfreq])
        variance = sum((v-mean)**2 for v in values)/(n-1)
        summary[c] = {"n":n,"mean":round(mean,4),"median":statistics.median(values),"modus":modes,
          "min":min(s),"max":max(s),"range":max(s)-min(s),"q1":round(quantile(.25),4),"q3":round(quantile(.75),4),
          "iqr":round(quantile(.75)-quantile(.25),4),"variance_sample":round(variance,4),"sd_sample":round(math.sqrt(variance),4)}
    x=cols["Persepsi"]; y=cols["PD"]; n=len(x)
    mx=sum(x)/n; my=sum(y)/n
    ssx=sum((v-mx)**2 for v in x); ssy=sum((v-my)**2 for v in y)
    sxy=sum((x[i]-mx)*(y[i]-my) for i in range(n))
    b=sxy/ssx; a=my-b*mx; r=sxy/math.sqrt(ssx*ssy); r2=r*r
    predicted=[a+b*v for v in x]
    rmse=math.sqrt(sum((y[i]-predicted[i])**2 for i in range(n))/n)
    rows=[]
    for i,row in enumerate(DATA_UJI,1):
        item={"no":i}
        item.update({c:row[j] for j,c in enumerate(DATA_COLUMNS)})
        item["prediksi_PD"]=round(a+b*row[3],4)
        item["residual"]=round(row[4]-item["prediksi_PD"],4)
        rows.append(item)
    # Tukey fences for weight outlier screening
    q1=summary['berat']['q1']; q3=summary['berat']['q3']; iqr=q3-q1
    upper=q3+1.5*iqr; lower=q1-1.5*iqr
    weight_outliers=[{"no":i+1,"berat":row[2]} for i,row in enumerate(DATA_UJI) if row[2]<lower or row[2]>upper]
    return {"columns":DATA_COLUMNS,"rows":rows,"summary":summary,
      "regression":{"x":"Persepsi","y":"PD","intercept":round(a,6),"slope":round(b,6),"equation":f"PD_hat = {a:.4f} + {b:.4f} × Persepsi","r":round(r,4),"r2":round(r2,4),"r2_percent":round(r2*100,2),"rmse":round(rmse,4),"predictions":{str(v):round(a+b*v,4) for v in range(2,10)}},
      "weight_outlier_screen":{"q1":q1,"q3":q3,"iqr":round(iqr,4),"lower_fence":round(lower,4),"upper_fence":round(upper,4),"observations":weight_outliers},
      "insights":[
       "Rata-rata PD (7,00) sedikit lebih tinggi daripada rata-rata Persepsi (6,57); kedua skala diasumsikan sebanding hanya jika definisi skala memang sama.",
       "Persepsi dan PD memiliki korelasi positif sedang (r ≈ 0,493). Ini menunjukkan asosiasi pada sampel, bukan bukti bahwa Persepsi menyebabkan PD.",
       "Model linear Persepsi → PD memiliki R² ≈ 24,33%; sebagian besar variasi PD belum dijelaskan oleh Persepsi saja.",
       "Berat memiliki rata-rata 63,20 dan median 58,00. Nilai 130 dan 140 terdeteksi di atas batas atas IQR (80,875); periksa data sumber/unit sebelum memutuskan apakah salah input atau nilai nyata.",
       "Tinggi rata-rata 167,03 dan median 168,00. Kolom jam memiliki rata-rata 5,23 dan median 6,00, tetapi arti dan satuannya perlu dikonfirmasi dari pembuat data."
      ]}

@app.route("/data-uji")
def data_uji_page():
    return render_template("data_uji.html")

@app.route("/api/data-uji")
def api_data_uji():
    return jsonify(data_uji_analisis())


if __name__ == "__main__":
    print("=" * 60)
    print("  DASHBOARD STATISTIK DESKRIPTIF")
    print("  Buka browser: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="127.0.0.1", port=5000)
