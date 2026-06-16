# Customer Churn Rate Analytics Dashboard (Donut Shop)

Sebuah aplikasi dashboard interaktif berbasis web yang dibangun menggunakan **Streamlit**, **Pandas**, dan **Plotly Express**. Dashboard ini berfungsi sebagai simulator data makro historis sekaligus mesin analisis perilaku konsumen (*customer behavioral analytics*) untuk memantau retensi, pergerakan omset, tren loyalitas, serta menghitung persentase retensi pelanggan (*Churn Rate*) dari bulan ke bulan secara otomatis.

By : **Alif Faqih**


## Fitur Dashboard

* **Advanced Historical Data Simulator**: Generator data otomatis yang mensimulasikan transaksi penjualan dari Juni 2018 hingga Juni 2026 berdasarkan pemodelan profil loyalitas konsumen (*Super Fans*, *Pelanggan Rutin*, dan *One-Hit Wonder*) serta penyesuaian faktor eksternal (seperti efek musiman bulan Desember dan anomali tren pasar tahunan).
* **Automated Churn Analytics**: Algoritma cerdas yang membandingkan irisan himpunan data pelanggan unik (`Customer_ID`) antar periode bulan berjalan untuk memetakan metrik:
    * *Retained Customers* (Pelanggan lama yang kembali belanja).
    * *Churned Customers* (Pelanggan yang absen/kabur pada bulan berjalan).
    * *Churn Rate (%)* (Rasio kehilangan pelanggan).
* **Interactive Business Intelligence Charts**: Visualisasi pergerakan tren *churn rate* berkala menggunakan *Line Chart* interaktif lengkap dengan fitur *unified hover*, serta visualisasi pertumbuhan basis pasar aktif melalui *Stacked Bar Chart*.
* **Dynamic Sidebar Filter**: Fasilitas penyaringan data berbasis multi-seleksi tahun kerja yang secara adaptif mengoptimalkan seluruh visualisasi grafik, tabel *overview*, dan metrik eksekutif tanpa perlu memuat ulang data induk.
* **Modern UI Components**: Penggunaan elemen antarmuka terbaru dari Streamlit seperti kontainer berbatasan (`st.container(border=True)`), indikator pemrosesan (`st.spinner`), visualisasi progres bar langsung di dalam tabel data (`st.column_config.ProgressColumn`), serta sistem notifikasi toast (`st.toast`).



##  Arsitektur & Spesifikasi Teknologi

* **Framework Antarmuka**: Streamlit (v1.35.0+)
* **Pusat Pengolahan Data**: Pandas (v2.0.0+)
* **Visualisasi Grafis**: Plotly Express (v5.15.0+)
* **Mesin Pengacak Probabilitas**: Python Random & Datetime Modules
* **Bahasa Pemrograman**: Python 3.10+



## Rumus Finansial & Logika Bisnis

Sistem menghitung status retensi konsumen menggunakan teori himpunan matematika pada daftar `Customer_ID` unik yang bertransaksi pada Periode Bulan Lalu ($M_{t-1}$) dan Periode Bulan Ini ($M_t$):

1. **Pelanggan Aktif Bulan Lalu**: 
   $$Total\ Aktif = |M_{t-1}|$$
2. **Kembali Belanja (Retained)**: 
   $$Retained = |M_{t-1} \cap M_t|$$
3. **Kabur / Absen (Churn)**: 
   $$Churn = |M_{t-1} - M_t|$$
4. **Churn Rate (%)**: 
   $$Churn\ Rate = \left( \frac{Total\ Churn}{Total\ Aktif\ Bulan\ Lalu} \right) \times 100\%$$

##  Flowchart Alur Program

Berikut adalah diagram alir proses sistem (Simulator, Analisis Sesi, hingga Visualisasi UI):

```mermaid
graph TD
    A([START]) --> B[Set Page Configuration 'Wide Layout']
    B --> C{Apakah st.session_state<br>'master_data' sudah ada?}
    
    C -- Tidak --> D[Tampilkan Pesan:<br>'Klik tombol Generate di sidebar']
    D --> E[Sistem Menunggu Input Tombol Sidebar]
    
    E --> F{Tombol Mana yang<br>Di-klik Pengguna?}
    F -- RESET --> G[Bersihkan Memori Sesi & Cache<br>Panggil st.rerun] --> B
    F -- GENERATE --> H[Jalankan Fungsi:<br>generate_historical_macro_data]
    
    H --> H1[Looping Bulanan: Jun 2018 - Jun 2026]
    H1 --> H2[Terapkan Faktor Musiman & Tren Penjualan]
    H2 --> H3[Akuisisi ID Konsumen Baru & Profil Loyalitas]
    H3 --> H4[Simulasikan Frekuensi Belanja, Box & Total Bayar]
    H4 --> I[Simpan DataFrame Hasil ke Sesi Master Data] --> J
    
    C -- Ya --> J[Muat Data dari st.session_state'master_data']
    
    J --> K[Tampilkan Filter Sidebar: Multi-select Tahun]
    K --> L[Filter Data Transaksi Berdasarkan Tahun Terpilih]
    
    L --> M[Jalankan Fungsi:<br>hitung_monthly_churn_report]
    M --> M1[Bandingkan Set Customer_ID Bulan Lalu vs Bulan Ini]
    M1 --> M2[Hitung Retained, Churn Volume & Churn Rate %]
    M2 --> N[Hasilkan DataFrame Churn Report]
    
    N --> O{Apakah Data Terfilter<br>Kosong?}
    O -- Ya --> P[Tampilkan Pesan Peringatan:<br>'Datanya kosong, centang minimal satu tahun'] --> E
    O -- Tidak --> Q[Render Metrik: Total Pelanggan, Nota, Omzet, Avg Churn]
    
    Q --> R[Render Plotly Line Chart: Tren Churn Rate]
    R --> S[Render Tabel Overview Data dengan Progress Bar]
    S --> T[Render Plotly Bar Chart: Distribusi Konsumen Aktif]
    T --> E