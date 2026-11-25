# 🍲 MBG PantauSuhu AI — Prediksi Suhu & Risiko Basi Makanan

Aplikasi web interaktif berbasis **Machine Learning** dan **Streamlit** untuk memperkirakan suhu makanan **Program Makan Bergizi Gratis (MBG)** saat tiba di sekolah serta mendeteksi risiko makanan menjadi basi selama perjalanan dari dapur pengiriman (SPPG) ke lokasi penerima.

---

## 🎯 Latar Belakang & Tujuan

Dalam distribusi Program Makan Bergizi Gratis (MBG), makanan yang sudah dimasak di dapur pusat harus tiba di sekolah dalam kondisi hangat dan aman dikonsumsi. Berdasarkan standar **Badan Gizi Nasional (BGN)**, suhu inti makanan saat tiba minimal harus **60°C** untuk mencegah pertumbuhan bakteri yang membuat makanan cepat dingin atau basi.

Aplikasi **MBG PantauSuhu AI** membantu pengelola dapur dan tim logistik untuk:

1. **Memperkirakan suhu makanan saat tiba** di sekolah berdasarkan jarak, lama perjalanan, jenis kendaraan pengantar, dan wilayah.
2. **Mendeteksi tingkat risiko basi** (skala 0–10) sebelum pengiriman dilakukan.
3. **Memberikan saran perbaikan logistik** otomatis jika suhu makanan diprediksi turun di bawah 60°C.

---

## ✨ Fitur Utama Aplikasi

* **Simulasi Cek Suhu & Risiko Basi:** Masukkan data wilayah, jenis lauk, kapasitas dapur, kendaraan pengantar, jarak (km), dan waktu perjalanan (menit) untuk langsung melihat perkiraan suhu saat tiba.
* **Indikator Kelayakan Otomatis:** Menampilkan status **AMAN DIMAKAN (≥ 60°C)** atau **BERISIKO BASI (< 60°C)** beserta kisaran fluktuasi suhu.
* **Wawasan Data Nasional per Wilayah:** Grafik dan tabel perbandingan rata-rata suhu kedatangan, skor risiko basi, dan persentase sisa makanan di berbagai kategori wilayah Indonesia (Jawa Metropolitan, Luar Jawa Urban, Pedesaan/Kepulauan, hingga Wilayah 3T).
* **Unduh Laporan (.CSV):** Hasil pengecekan suhu dapat langsung diunduh dalam format file `.csv` untuk dokumentasi audit harian.
* **Mode Gelap & Terang (Dark/Light Mode):** Tampilan antarmuka modern yang nyaman digunakan di berbagai perangkat.

---

## 📊 Sumber Data & Performa Model AI

Model kecerdasan buatan pada proyek ini dilatih menggunakan dataset publik **[Indonesia Makan Bergizi Gratis (MBG) Telemetry 2026](https://www.kaggle.com/datasets/luthfimuthathohirin/indonesia-makan-bergizi-gratis-mbg-telemetry)** (`indonesia_mbg_nationwide_enriched_2026.csv`) dari Kaggle yang mencakup **13.000 catatan pengiriman** di **38 provinsi** di Indonesia.

* **Link Dataset:** [Unduh di Kaggle (Indonesia MBG Telemetry)](https://www.kaggle.com/datasets/luthfimuthathohirin/indonesia-makan-bergizi-gratis-mbg-telemetry)
* **Algoritma:** Random Forest Regressor (100 Trees, terkompresi agar ringan untuk deployment web)
* **Ketepatan Prediksi Suhu ($R^2$ Score):** **~87%** (Toleransi selisih rata-rata **± 1,5°C**)
* **Ketepatan Prediksi Risiko Basi ($R^2$ Score):** **~96%**

---

## 📁 Struktur Folder Proyek

```text
mbg-pantausuhu-ai/
├── model/
│   ├── model_suhu_mbg.pkl                         # Model AI prediksi suhu kedatangan
│   ├── model_spoilage_mbg.pkl                     # Model AI prediksi skor risiko basi
│   └── metadata.json                              # Informasi opsi dropdown & metrik akurasi
├── train_model_mbg_thermal_guard.ipynb            # Notebook eksplorasi data & pelatihan model
├── app.py                                         # Kode utama aplikasi web Streamlit
├── style.css                                      # Desain tampilan (CSS) aplikasi
├── requirements.txt                               # Daftar pustaka Python yang dibutuhkan
└── README.md                                      # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan di Komputer Lokal

1. **Unduh (Clone) Repositori Ini**

   ```bash
   git clone https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git
   cd NAMA_REPO_KAMU
   ```

2. **Buat Virtual Environment & Instal Pustaka**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Latih Model (Opsional jika folder `model/` sudah tersedia)**
   Unduh dataset dari [tautan Kaggle ini](https://www.kaggle.com/datasets/luthfimuthathohirin/indonesia-makan-bergizi-gratis-mbg-telemetry), letakkan file `indonesia_mbg_nationwide_enriched_2026.csv` di dalam folder `dataset/`, buka file `train_model_mbg_thermal_guard.ipynb` di VS Code atau Jupyter Notebook, lalu jalankan seluruh sel (*Run All*) untuk menghasilkan file model di dalam folder `model/`.

4. **Jalankan Aplikasi Web Streamlit**

   ```bash
   streamlit run app.py
   ```

   Buka browser dan akses alamat lokal yang muncul (biasanya `http://localhost:8501`).

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.10+
* **Antarmuka Web:** Streamlit & Custom CSS
* **Machine Learning & Data:** Scikit-Learn, Pandas, NumPy, Joblib
* **Visualisasi Eksplorasi Data:** Matplotlib & Seaborn