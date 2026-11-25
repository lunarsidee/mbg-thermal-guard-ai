import json
import numpy as np
import pandas as pd
import joblib
import streamlit as st

st.set_page_config(
    page_title="MBG PantauSuhu AI | Prediksi Suhu & Risiko Basi",
    page_icon="🍲",
    layout="wide"
)

def load_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

@st.cache_resource
def load_assets():
    model_temp = joblib.load("model/model_suhu_mbg.pkl")
    model_spoil = joblib.load("model/model_spoilage_mbg.pkl")
    with open("model/metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return model_temp, model_spoil, metadata

model_temp, model_spoil, metadata = load_assets()
opts = metadata["options"]
metrics = metadata["metrics"]

DEFAULT_PAYLOAD = {
    "regional_cluster": "Jawa Metropolitan",
    "province": "Jawa Tengah",
    "beneficiary_category": "Siswa SD / Madrasah Ibtidaiyah",
    "protein_type": "Daging Ayam Broiler",
    "delivery_transport_mode": "Mobil Pickup Termal",
    "kitchen_daily_capacity_portions": 1800,
    "delivery_distance_km": 6.5,
    "transit_time_minutes": 25
}

if "mbg_submitted" not in st.session_state:
    st.session_state.mbg_submitted = DEFAULT_PAYLOAD.copy()

def reset_form():
    st.session_state.mbg_submitted = DEFAULT_PAYLOAD.copy()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pengaturan Tampilan")
    dark_mode = st.toggle("🌙 Mode Gelap (Dark Mode)", value=True)
    if not dark_mode:
        st.markdown("""
            <style>
            .stApp { background-color: #f8fafc; color: #0f172a; }
            .info-badge { background: #ffffff; color: #0f172a; border-color: #cbd5e1; }
            .info-badge span { color: #0284c7; }
            .mini-card { background: #ffffff; border-color: #e2e8f0; }
            </style>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🌡️ Batas Suhu Aman Makanan")
    safe_threshold = st.slider("Suhu Hangat Minimum (°C)", min_value=55.0, max_value=65.0, value=60.0, step=0.5)
    st.caption("Standar Badan Gizi Nasional (BGN) mewajibkan suhu makanan tiba minimal **60°C** agar tetap hangat, higienis, dan tidak cepat basi.")

    st.divider()
    st.subheader("📊 Akurasi Sistem Prediksi")
    st.metric("Ketepatan Prediksi Suhu (R²)", f"{metrics['r2_temp']}%")
    st.metric("Selisih Rata-Rata Suhu", f"± {metrics['medae_temp']} °C")
    st.metric("Ketepatan Prediksi Risiko Basi", f"{metrics['r2_spoil']}%")
    st.caption(f"Dilatih dari **{metrics['total_data']:,} data pengiriman** di **{metrics['total_provinces']} provinsi**.")

# --- HERO BANNER ---
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🍲 MBG PantauSuhu AI • Prediksi Suhu & Risiko Basi Makanan</div>
    <div class="hero-desc">
        Aplikasi untuk memperkirakan suhu makanan <b>Program Makan Bergizi Gratis (MBG)</b> saat tiba di sekolah 
        serta mendeteksi seberapa besar risiko makanan menjadi basi selama perjalanan dari dapur ke sekolah.
    </div>
    <div class="badge-row">
        <div class="info-badge">🤖 Metode AI: <span>Random Forest (200 Trees)</span></div>
        <div class="info-badge">🎯 Ketepatan Suhu: <span>{metrics['r2_temp']}%</span></div>
        <div class="info-badge">📉 Toleransi Selisih: <span>± {metrics['medae_temp']} °C</span></div>
        <div class="info-badge">📦 Total Data Latih: <span>{metrics['total_data']:,} Pengiriman</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_sim, tab_stats = st.tabs(["🌡️ Simulasi Cek Suhu & Risiko Basi", "📈 Data Suhu Makanan per Wilayah"])

with tab_sim:
    col_in, col_out = st.columns([1.15, 1], gap="large")

    with col_in:
        with st.container(border=True):
            st.subheader("📍 1. Wilayah & Penerima Makanan")
            c1, c2 = st.columns(2)
            with c1:
                cluster_list = opts["regional_cluster"]
                cluster = st.selectbox(
                    "Kategori Wilayah",
                    cluster_list,
                    index=cluster_list.index(DEFAULT_PAYLOAD["regional_cluster"])
                )
            with c2:
                prov_list = opts["cluster_to_provinces"][cluster]
                default_prov_idx = prov_list.index("Jawa Tengah") if "Jawa Tengah" in prov_list else 0
                province = st.selectbox("Provinsi", prov_list, index=default_prov_idx)

            c3, c4 = st.columns(2)
            with c3:
                ben_list = opts["beneficiary_category"]
                beneficiary = st.selectbox(
                    "Kelompok Penerima",
                    ben_list,
                    index=ben_list.index(DEFAULT_PAYLOAD["beneficiary_category"])
                )
            with c4:
                prot_list = opts["protein_type"]
                protein = st.selectbox(
                    "Menu Lauk Utama",
                    prot_list,
                    index=prot_list.index(DEFAULT_PAYLOAD["protein_type"])
                )

            st.divider()
            st.subheader("🚚 2. Kapasitas Dapur & Perjalanan")
            c5, c6 = st.columns(2)
            with c5:
                trans_list = opts["delivery_transport_mode"]
                transport = st.selectbox(
                    "Kendaraan Pengantar",
                    trans_list,
                    index=trans_list.index(DEFAULT_PAYLOAD["delivery_transport_mode"])
                )
            with c6:
                capacity = st.number_input(
                    "Jumlah Masakan Dapur (porsi/hari)",
                    min_value=500,
                    max_value=4000,
                    value=DEFAULT_PAYLOAD["kitchen_daily_capacity_portions"],
                    step=100
                )

            c7, c8 = st.columns(2)
            with c7:
                distance = st.number_input(
                    "Jarak Dapur ke Sekolah (km)",
                    min_value=0.5,
                    max_value=35.0,
                    value=DEFAULT_PAYLOAD["delivery_distance_km"],
                    step=0.5
                )
            with c8:
                transit = st.number_input(
                    "Lama Perjalanan (menit)",
                    min_value=5,
                    max_value=120,
                    value=DEFAULT_PAYLOAD["transit_time_minutes"],
                    step=1
                )

            st.write("")
            b1, b2 = st.columns([2.2, 1])
            with b1:
                submit_btn = st.button("🔍 Cek Suhu & Risiko Basi", type="primary", use_container_width=True)
            with b2:
                st.button("🔄 Reset", on_click=reset_form, use_container_width=True)

            if submit_btn:
                st.session_state.mbg_submitted = {
                    "regional_cluster": cluster,
                    "province": province,
                    "beneficiary_category": beneficiary,
                    "protein_type": protein,
                    "delivery_transport_mode": transport,
                    "kitchen_daily_capacity_portions": int(capacity),
                    "delivery_distance_km": float(distance),
                    "transit_time_minutes": int(transit)
                }
                st.toast("✅ Hasil prediksi suhu berhasil diperbarui!", icon="🌡️")

    with col_out:
        active = st.session_state.mbg_submitted
        input_df = pd.DataFrame([active])[metadata["features"]]

        prep_temp = model_temp.named_steps["preprocessor"]
        rf_temp = model_temp.named_steps["regressor"]
        X_tr = prep_temp.transform(input_df)
        tree_preds = np.array([t.predict(X_tr)[0] for t in rf_temp.estimators_])

        pred_temp = float(np.mean(tree_preds))
        low_temp = float(np.percentile(tree_preds, 25))
        high_temp = float(np.percentile(tree_preds, 75))

        pred_spoil = float(model_spoil.predict(input_df)[0])

        is_safe = pred_temp >= safe_threshold
        temp_class = "temp-value-safe" if is_safe else "temp-value-risk"
        pill_class = "status-pill-safe" if is_safe else "status-pill-risk"
        status_text = (
            f"✅ AMAN DIMAKAN (Suhu Hangat ≥ {safe_threshold}°C)"
            if is_safe else
            f"⚠️ BERISIKO BASI / TERLALU DINGIN (< {safe_threshold}°C)"
        )

        st.subheader("🎯 Hasil Pengecekan Suhu Makanan")
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">{active['province']} • {active['delivery_transport_mode']}</div>
            <div class="{temp_class}">{pred_temp:.1f} °C</div>
            <div class="{pill_class}">{status_text}</div>
            <div class="range-box">
                <div class="range-title">📊 Perkiraan Kisaran Suhu Saat Tiba</div>
                <div class="range-values">
                    <span>Terendah: {low_temp:.1f} °C</span>
                    <span>Tertinggi: {high_temp:.1f} °C</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if pred_spoil < 2.5:
            risk_label = "Rendah"
        elif pred_spoil < 5.0:
            risk_label = "Sedang"
        else:
            risk_label = "Tinggi"

        speed_kmh = active["delivery_distance_km"] / (active["transit_time_minutes"] / 60.0)
        margin_bgn = pred_temp - safe_threshold

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="mini-card">
                <div class="mini-card-label">Tingkat Risiko Basi</div>
                <div class="mini-card-val">{pred_spoil:.2f}/10 ({risk_label})</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="mini-card">
                <div class="mini-card-label">Selisih Batas Aman</div>
                <div class="mini-card-val">{'+' if margin_bgn >= 0 else ''}{margin_bgn:.1f} °C</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="mini-card">
                <div class="mini-card-label">Kecepatan Antar</div>
                <div class="mini-card-val">{speed_kmh:.1f} km/jam</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        if not is_safe or pred_spoil >= 4.0:
            st.warning(
                "**Saran Perbaikan Pengiriman:** Suhu makanan saat tiba terlalu dingin dan berisiko cepat basi. "
                "Gunakan **kotak penahan panas (termos makanan)** yang tertutup rapat atau percepat waktu antar di bawah 30 menit."
            )

        export_df = pd.DataFrame([{
            **active,
            "Prediksi_Suhu_Tiba_C": round(pred_temp, 2),
            "Skor_Risiko_Basi_0_10": round(pred_spoil, 2),
            "Kategori_Risiko": risk_label,
            "Status_Keamanan": "AMAN" if is_safe else "BERISIKO_BASI"
        }])
        st.download_button(
            label="📥 Unduh Laporan Pengecekan Suhu (.CSV)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name=f"laporan_suhu_mbg_{active['province'].lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )

with tab_stats:
    st.subheader("📈 Perbandingan Suhu Makanan Tiba per Kategori Wilayah")
    stats_df = pd.DataFrame(metadata["cluster_stats"])
    stats_df["Rata-Rata Suhu (°C)"] = stats_df["mean_temp"].round(2)
    stats_df["Suhu Tengah (°C)"] = stats_df["median_temp"].round(2)
    stats_df["Skor Risiko Basi"] = stats_df["mean_spoilage"].round(2)
    stats_df["Sisa Makanan (%)"] = stats_df["mean_waste"].round(2)
    stats_df = stats_df.rename(columns={"regional_cluster": "Kategori Wilayah", "count": "Jumlah Pengiriman"})

    c_left, c_right = st.columns([1.2, 1.3], gap="large")
    with c_left:
        st.bar_chart(stats_df.set_index("Kategori Wilayah")["Rata-Rata Suhu (°C)"], color="#38bdf8", height=360)
    with c_right:
        st.dataframe(
            stats_df[["Kategori Wilayah", "Rata-Rata Suhu (°C)", "Suhu Tengah (°C)", "Skor Risiko Basi", "Sisa Makanan (%)", "Jumlah Pengiriman"]],
            use_container_width=True,
            hide_index=True
        )