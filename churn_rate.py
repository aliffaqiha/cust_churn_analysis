import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime, timedelta

def generate_historical_macro_data():
    START_DATE = datetime(2018, 6, 1)
    END_DATE = datetime(2026, 6, 1)
    list_all_transaksi = []
    
    tipe_loyalitas_pool = ["Super Fans", "Pelanggan Rutin", "One-Hit Wonder"]
    opsi_platform = ["WhatsApp Chat", "Instagram DM", "GoFood", "GrabFood", "ShopeeFood"]
    database_pelanggan_historis = []
    global_customer_counter = 1
    
    total_bulan = (END_DATE.year - START_DATE.year) * 12 + (END_DATE.month - START_DATE.month)
    
    for bulan_ke in range(total_bulan):
        tgl_bulan_ini = START_DATE + timedelta(days=bulan_ke * 30.5)
        if tgl_bulan_ini >= END_DATE:
            break
            
        str_bulan_ini = tgl_bulan_ini.strftime("%Y-%m")
        thn_bulan_ini = tgl_bulan_ini.strftime("%Y")
        
        faktor_akuisisi_baru = 1.0  
        probabilitas_absen_belanja = 0.3  
        
        if tgl_bulan_ini.month == 12:
            faktor_akuisisi_baru = 1.5
            probabilitas_absen_belanja = 0.12
            
        if thn_bulan_ini in ["2020", "2021"]: 
            faktor_akuisisi_baru = 1.8 
            probabilitas_absen_belanja = 0.45
        elif thn_bulan_ini == "2023":
            probabilitas_absen_belanja = 0.55
        elif thn_bulan_ini == "2025" and tgl_bulan_ini.month == 6:
            faktor_akuisisi_baru = 3.0

        bobot_loyalitas = [25, 55, 20] 
        jumlah_baru_base = random.randint(15, 35)
        jumlah_baru_riil = int(jumlah_baru_base * faktor_akuisisi_baru)
        
        for _ in range(jumlah_baru_riil):
            database_pelanggan_historis.append({
                "Customer_ID": f"CUST-{str(global_customer_counter).zfill(5)}",
                "Tipe_Loyalitas": random.choices(tipe_loyalitas_pool, weights=bobot_loyalitas)[0]
            })
            global_customer_counter += 1
            
        for pelanggan in database_pelanggan_historis:
            cust_id = pelanggan["Customer_ID"]
            tipe_loyal = pelanggan["Tipe_Loyalitas"]
            
            if tipe_loyal == "Super Fans":
                if (thn_bulan_ini == "2023") and random.random() < 0.25:
                    frekuensi_bulan_ini = 0
                else:
                    frekuensi_bulan_ini = random.randint(2, 4)
            elif tipe_loyal == "Pelanggan Rutin":
                if random.random() < probabilitas_absen_belanja:
                    frekuensi_bulan_ini = 0
                else:
                    frekuensi_bulan_ini = random.randint(1, 2)
            else:  
                is_baru_bulan_ini = cust_id in [p["Customer_ID"] for p in database_pelanggan_historis[-jumlah_baru_riil:]]
                frekuensi_bulan_ini = 1 if is_baru_bulan_ini else 0
                
            for f in range(frekuensi_bulan_ini):
                hari_acak = random.randint(0, 27)
                tanggal_transaksi = tgl_bulan_ini + timedelta(days=hari_acak)
                jumlah_box = random.choices([1, 2, 3], weights=[65, 25, 10])[0]
                
                list_all_transaksi.append({
                    "Customer_ID": cust_id,
                    "Tanggal_Transaksi": tanggal_transaksi,
                    "Tahun_Periode": thn_bulan_ini,
                    "Bulan_Periode": str_bulan_ini,
                    "Jumlah_Box": jumlah_box,
                    "Total_Bayar": jumlah_box * 60000,
                    "Platform_Order": random.choice(opsi_platform)
                })
                
    df_res = pd.DataFrame(list_all_transaksi)
    return df_res.sort_values(by="Tanggal_Transaksi").reset_index(drop=True)

def hitung_monthly_churn_report(df_transaksi):
    bulan_unik = sorted(df_transaksi["Bulan_Periode"].unique())
    log_report = []
    
    if len(bulan_unik) < 2:
        return pd.DataFrame(columns=["Bulan", "Tahun", "Pelanggan Aktif Bulan Lalu", "Kembali Belanja (Retained)", "Kabur/Absen (Churn)", "Churn Rate (%)"])
    
    for i in range(1, len(bulan_unik)):
        bulan_lalu = bulan_unik[i-1]
        bulan_ini = bulan_unik[i]
        
        pelanggan_bulan_lalu = set(df_transaksi[df_transaksi["Bulan_Periode"] == bulan_lalu]["Customer_ID"])
        pelanggan_bulan_ini = set(df_transaksi[df_transaksi["Bulan_Periode"] == bulan_ini]["Customer_ID"])
        
        pelanggan_churn = pelanggan_bulan_lalu - pelanggan_bulan_ini
        pelanggan_kembali = pelanggan_bulan_lalu & pelanggan_bulan_ini
        
        total_aktif_lalu = len(pelanggan_bulan_lalu)
        total_churn = len(pelanggan_churn)
        total_kembali = len(pelanggan_kembali)
        
        churn_rate = (total_churn / total_aktif_lalu * 100) if total_aktif_lalu > 0 else 0
        
        log_report.append({
            "Bulan": bulan_ini,
            "Tahun": bulan_ini.split("-")[0],
            "Pelanggan Aktif Bulan Lalu": total_aktif_lalu,
            "Kembali Belanja (Retained)": total_kembali,
            "Kabur/Absen (Churn)": total_churn,
            "Churn Rate (%)": round(churn_rate, 1)
        })
        
    return pd.DataFrame(log_report)

st.set_page_config(page_title="Donut Shop Analytics", layout="wide")

if "master_data" not in st.session_state:
    st.session_state["master_data"] = None

with st.sidebar:
    st.subheader("Pengaturan Data")
    st.caption("Klik generate untuk bikin data simulasi penjualan 8 tahun.")
    
    with st.container(border=True):
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Generate", type="primary", use_container_width=True):
                with st.spinner("Mengacak data..."):
                    st.session_state["master_data"] = generate_historical_macro_data()
                st.toast("Data simulasi siap dianalisis!")
        with col_btn2:
            if st.button("Reset", type="secondary", use_container_width=True):
                st.session_state["master_data"] = None
                st.cache_data.clear()
                st.rerun()

if st.session_state["master_data"] is None:
    st.title("Donut Shop Customer Analytics")
    st.info("Dashboard masih kosong nih. Yuk, klik tombol 'Generate' di sidebar kiri buat memproses simulasi datanya.")
else:
    df_master_transaksi = st.session_state["master_data"]

    with st.sidebar:
        st.write("")
        st.subheader("Filter Analisis")
        tahun_tersedia = sorted(df_master_transaksi["Tahun_Periode"].unique())
        tahun_terpilih = st.multiselect(
            "Pilih Tahun Kerja:",
            options=tahun_tersedia,
            default=tahun_tersedia,
            placeholder="Pilih tahun..."
        )

    df_filtered_transaksi = df_master_transaksi[df_master_transaksi["Tahun_Periode"].isin(tahun_terpilih)]
    df_churn_tabel = hitung_monthly_churn_report(df_filtered_transaksi)

    if df_filtered_transaksi.empty:
        st.title("Donut Shop Customer Analytics")
        st.warning("Datanya kosong. Coba centang minimal satu tahun di menu filter sidebar ya.")
    else:
        st.title("Donut Shop Customer Analytics")
        st.caption("Dashboard personal untuk memantau retensi, omset, dan tren loyalitas pelanggan.")
        st.write("")

        total_pelanggan_unik = df_filtered_transaksi["Customer_ID"].nunique()
        total_omzet = df_filtered_transaksi["Total_Bayar"].sum()
        rerata_churn = df_churn_tabel["Churn Rate (%)"].mean() if not df_churn_tabel.empty else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1.container(border=True):
            st.metric("Total Pelanggan", f"{total_pelanggan_unik:,} orang")
        with col2.container(border=True):
            st.metric("Total Nota Keluar", f"{len(df_filtered_transaksi):,} transaksi")
        with col3.container(border=True):
            st.metric("Omzet Penjualan", f"Rp {total_omzet:,}")
        with col4.container(border=True):
            st.metric("Rata-rata Churn Bulanan", f"{round(rerata_churn, 1)}%")

        st.write("")
        st.subheader("Tren Naik Turun Churn Rate (%)")
        
        if not df_churn_tabel.empty:
            fig_churn = px.line(
                df_churn_tabel, 
                x="Bulan", 
                y="Churn Rate (%)", 
                markers=True,
                color_discrete_sequence=["#0f172a"]
            )
            fig_churn.update_traces(line=dict(width=2))
            fig_churn.update_layout(
                margin=dict(l=20, r=20, t=10, b=20),
                hovermode="x unified",
                xaxis=dict(title="Periode", tickangle=45, gridcolor="#f1f5f9"),
                yaxis=dict(title="Churn Rate (%)", gridcolor="#f1f5f9"),
                plot_bgcolor="white"
            )
            st.plotly_chart(fig_churn, use_container_width=True)
        else:
            st.info("Pilih rentang tahun yang lebih panjang untuk melihat pergerakan grafik tren bulanan.")

        st.write("")
        col_grid_left, col_grid_right = st.columns([5, 4])

        with col_grid_left:
            st.subheader("Overview Data")
            
            df_display = df_churn_tabel.sort_values(by="Bulan", ascending=False).copy()
            
            styled_df = df_display.style.background_gradient(
                cmap="Reds", 
                subset=["Kabur/Absen (Churn)", "Churn Rate (%)"]
            ).format({
                "Pelanggan Aktif Bulan Lalu": "{:,}",
                "Kembali Belanja (Retained)": "{:,}",
                "Kabur/Absen (Churn)": "{:,}",
                "Churn Rate (%)": "{:.1f}%"
            })
            
            st.dataframe(
                styled_df, 
                use_container_width=True, 
                hide_index=True, 
                height=400,
                column_config={
                    "Bulan": "Periode",
                    "Tahun": "Tahun",
                    "Pelanggan Aktif Bulan Lalu": "Aktif Bulan Lalu",
                    "Kembali Belanja (Retained)": "Aktif Sekarang",
                    "Kabur/Absen (Churn)": "Pelanggan Kabur",
                    "Churn Rate (%)": "Churn Rate"
                }
            )

        with col_grid_right:
            st.subheader("Distribusi Jumlah Konsumen Aktif")
            if not df_churn_tabel.empty:
                fig_growth = px.bar(
                    df_churn_tabel,
                    x="Bulan",
                    y="Pelanggan Aktif Bulan Lalu",
                    color="Tahun",
                    color_discrete_sequence=px.colors.qualitative.G10
                )
                fig_growth.update_layout(
                    margin=dict(l=20, r=20, t=10, b=20),
                    xaxis=dict(title="Periode", tickangle=45, gridcolor="#f1f5f9"),
                    yaxis=dict(title="Konsumen Aktif", gridcolor="#f1f5f9"),
                    plot_bgcolor="white",
                    showlegend=True,
                    legend=dict(title="Tahun", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_growth, use_container_width=True)
            else:
                st.info("Data tidak cukup untuk menampilkan peta sebaran volume pasar.")