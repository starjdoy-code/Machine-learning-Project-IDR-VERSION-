import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from datetime import date

st.set_page_config(page_title="Simulasi Penjualan", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

*, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer { visibility: hidden; }
header { visibility: hidden; }
/* Keep sidebar toggle button visible */
[data-testid="collapsedControl"],
button[kind="header"],
section[data-testid="stSidebar"] > div:first-child button { visibility: visible !important; }
.stApp { background: #f0f4f8; }

/* Force sidebar open and visible */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: none !important;
    min-width: 320px !important;
    max-width: 380px !important;
}

[data-testid="stSidebar"] { background: #1a2332 !important; border-right: none !important; }
[data-testid="stSidebar"] * { color: #c8d8e8 !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #7a9ab8 !important; font-size: .78rem !important; }
[data-testid="stSidebar"] .stMarkdown strong {
    color: #e8f0f8 !important; font-size: .68rem !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: .12em;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] .stSelectbox > div { background: #243040 !important; }
[data-testid="stForm"] { border: none !important; background: transparent !important; box-shadow: none !important; padding: 0 !important; }

div[data-testid="stFormSubmitButton"] button {
    width: 100%; background: #2563eb; color: #fff !important;
    border: none; border-radius: 6px;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: .82rem !important; font-weight: 600 !important;
    letter-spacing: .04em; padding: 13px; cursor: pointer;
}
div[data-testid="stFormSubmitButton"] button:hover { background: #1d4ed8; }
div[data-testid="stFormSubmitButton"] button p { color: #fff !important; }

[data-testid="stMetric"] {
    background: #ffffff; border: none; border-radius: 8px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}
[data-testid="stMetricLabel"] { font-size:.7rem !important; font-weight:600 !important; text-transform:uppercase !important; letter-spacing:.1em !important; color:#64748b !important; }
[data-testid="stMetricValue"] { font-family:'IBM Plex Mono',monospace !important; font-size:1.45rem !important; color:#0f172a !important; }
[data-testid="stMetricDelta"] { font-size:.72rem !important; color:#2563eb !important; }

h1 { font-size:1.6rem !important; font-weight:700 !important; color:#0f172a !important; letter-spacing:-.01em !important; }
h2, h3 { font-size:.72rem !important; font-weight:600 !important; color:#64748b !important; text-transform:uppercase !important; letter-spacing:.12em !important; }
hr { border:none; border-top:1px solid #e2e8f0; margin:1.2rem 0; }

.hero-card {
    background: #2563eb; border-radius: 12px; padding: 36px 40px;
    color: white; position: relative; overflow: hidden;
}
.hero-stats { display:flex; gap:10px; margin-top:18px; flex-wrap:wrap; }
.hero-stat {
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px; padding: 10px 16px; flex: 1; min-width: 130px;
    display: flex; flex-direction: column; justify-content: center; align-items: flex-start;
}
.hero-stat.center { align-items: center; text-align: center; }
.hero-stat-label { font-size:.62rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; opacity:.7; margin-bottom:4px; white-space: nowrap; }
.hero-stat-value { font-family:'IBM Plex Mono',monospace; font-size:.95rem; font-weight:600; white-space: nowrap; }
.hero-card::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:160px; height:160px; background:rgba(255,255,255,0.06); border-radius:50%;
}
.hero-card::before {
    content:''; position:absolute; bottom:-20px; right:60px;
    width:100px; height:100px; background:rgba(255,255,255,0.04); border-radius:50%;
}
.hero-eyebrow { font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.14em; opacity:.7; margin-bottom:6px; }
.hero-amount { font-family:'IBM Plex Mono',monospace; font-size:3.4rem; font-weight:600; line-height:1; margin-bottom:8px; letter-spacing:-.02em; }
.hero-model { font-size:.75rem; opacity:.65; font-family:'IBM Plex Mono',monospace; }
.conf-row { display:flex; align-items:center; gap:10px; margin-top:14px; }
.conf-label { font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.1em; opacity:.7; white-space:nowrap; }
.conf-track { flex:1; background:rgba(255,255,255,.2); height:6px; border-radius:3px; }
.conf-fill { height:6px; border-radius:3px; background:rgba(255,255,255,.9); }
.conf-pct { font-family:'IBM Plex Mono',monospace; font-size:.75rem; white-space:nowrap; }

.status-kpi {
    background:#fff; border-radius:10px; padding:20px 22px;
    box-shadow:0 1px 3px rgba(0,0,0,0.08); border-top:4px solid; height:100%;
}
.status-high { border-top-color:#10b981; }
.status-mid  { border-top-color:#f59e0b; }
.status-low  { border-top-color:#ef4444; }
.status-badge { display:inline-block; padding:2px 10px; border-radius:12px; font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }
.status-high .status-badge { background:#d1fae5; color:#065f46; }
.status-mid  .status-badge { background:#fef3c7; color:#92400e; }
.status-low  .status-badge { background:#fee2e2; color:#991b1b; }
.status-title-text { font-size:.95rem; font-weight:600; color:#0f172a; margin-bottom:4px; }
.status-body { font-size:.82rem; color:#64748b; line-height:1.5; }

.pill {
    display:inline-block; background:#fff; border:1px solid #e2e8f0;
    border-radius:20px; padding:4px 12px; font-size:.72rem;
    color:#475569; margin:2px; font-weight:500;
}

.fi-row { margin-bottom:12px; }
.fi-label { font-size:.78rem; color:#334155; margin-bottom:4px; display:flex; justify-content:space-between; font-weight:500; }
.fi-score { color:#94a3b8; font-family:'IBM Plex Mono',monospace; font-size:.72rem; }
.fi-track { background:#e2e8f0; border-radius:3px; height:6px; }
.fi-fill { height:6px; border-radius:3px; background:linear-gradient(90deg,#2563eb,#7c3aed); }

.trow { display:flex; align-items:center; gap:10px; padding:10px 14px; font-size:.82rem; color:#475569; }
.trow:not(:last-child) { border-bottom:1px solid #f1f5f9; }
.dp { width:9px; height:9px; border-radius:50%; display:inline-block; flex-shrink:0; }
.section-card { background:#fff; border-radius:10px; padding:22px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.06); margin-bottom:12px; }

.eval-card {
    background:#ffffff; border-radius:10px; padding:20px 22px;
    box-shadow:0 1px 3px rgba(0,0,0,0.08),0 1px 2px rgba(0,0,0,0.04);
    border-top:4px solid #e2e8f0; height:100%;
}
.eval-card.model { border-top-color:#7c3aed; }
.eval-card.mae   { border-top-color:#2563eb; }
.eval-card.rmse  { border-top-color:#0891b2; }
.eval-card.r2    { border-top-color:#10b981; }
.eval-eyebrow { font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; color:#64748b; margin-bottom:8px; }
.eval-value { font-family:'IBM Plex Mono',monospace; font-size:1.5rem; font-weight:600; color:#0f172a; line-height:1.1; }
.eval-delta { display:inline-block; margin-top:7px; background:#dbeafe; color:#1d4ed8; font-size:.7rem; font-weight:600; padding:3px 9px; border-radius:12px; font-family:'IBM Plex Mono',monospace; }
.eval-delta.ok   { background:#d1fae5; color:#065f46; }
.eval-delta.warn { background:#fef3c7; color:#92400e; }

.threshold-strip { background:#fff; border-radius:10px; padding:0 8px; box-shadow:0 1px 3px rgba(0,0,0,0.06); overflow:hidden; }

.section-title {
    font-size:.72rem; font-weight:700; color:#64748b;
    text-transform:uppercase; letter-spacing:.14em;
    display:flex; align-items:center; gap:8px; margin-bottom:12px;
}
.section-title::after { content:''; flex:1; height:1px; background:#e2e8f0; }

.disclaimer-box {
    background:#fffbeb; border:1px solid #fde68a; border-radius:8px;
    padding:14px 18px; font-size:.82rem; color:#78350f; line-height:1.6; margin-bottom:20px;
}
.disclaimer-box strong { color:#92400e; }
</style>
""", unsafe_allow_html=True)

# ── Konversi Mata Uang ────────────────────────────────────────────────────────
EUR_TO_IDR = 17_500  # Perbarui sesuai kurs terkini

# Label fitur ramah bisnis
FEAT_LABELS = {
    'Store': 'Profil Toko', 'DayOfWeek': 'Hari dalam Seminggu',
    'Promo': 'Promosi Aktif', 'StateHoliday': 'Hari Libur Nasional',
    'SchoolHoliday': 'Libur Sekolah', 'StoreType': 'Ukuran Toko',
    'Assortment': 'Ragam Produk', 'CompetitionDistance': 'Jarak ke Pesaing',
    'CompetitionOpenSinceMonth': 'Bulan Buka Pesaing',
    'CompetitionOpenSinceYear': 'Tahun Buka Pesaing',
    'Promo2': 'Promo Berulang', 'Promo2SinceWeek': 'Mulai Promo (Minggu)',
    'Promo2SinceYear': 'Mulai Promo (Tahun)',
    'PromoInterval': 'Musim Promo', 'Year': 'Tahun',
    'Month': 'Bulan', 'Day': 'Tanggal', 'WeekOfYear': 'Minggu ke-',
}

# ── Load Model ────────────────────────────────────────────────────────────────
import os
_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource(show_spinner="Memuat model...")
def load_model():
    m  = joblib.load(os.path.join(_DIR, 'model_rossman.pkl'))
    f  = joblib.load(os.path.join(_DIR, 'model_features.pkl'))
    ev = joblib.load(os.path.join(_DIR, 'eval_data.pkl'))
    fi = joblib.load(os.path.join(_DIR, 'feature_importance.pkl'))
    return m, f, ev, fi

try:
    model, FEATURES, ev, fi = load_model()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.info("Pastikan file .pkl berada di folder yang sama dengan app.py")
    st.stop()

# ── Grafik Statis ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def static_charts():
    fig_s = go.Figure()
    fig_s.add_trace(go.Scattergl(
        x=ev['y_aktual'], y=ev['y_prediksi'],
        mode='markers', name='Data Toko',
        marker=dict(color='#2563eb', size=3, opacity=0.3)
    ))
    lo = float(min(ev['y_aktual'].min(), ev['y_prediksi'].min()))
    hi = float(max(ev['y_aktual'].max(), ev['y_prediksi'].max()))
    fig_s.add_trace(go.Scatter(
        x=[lo, hi], y=[lo, hi], mode='lines', name='Prediksi Sempurna',
        line=dict(color='#7c3aed', dash='dash', width=1.5)
    ))
    fig_s.update_layout(
        paper_bgcolor='#fff', plot_bgcolor='#f8fafc',
        xaxis=dict(title='Aktual (indeks)', gridcolor='#f1f5f9',
                   tickfont=dict(family='IBM Plex Mono', size=11, color='#94a3b8')),
        yaxis=dict(title='Prediksi (indeks)', gridcolor='#f1f5f9',
                   tickfont=dict(family='IBM Plex Mono', size=11, color='#94a3b8')),
        title=dict(text=f"R² = {ev['r2']:.4f}", font=dict(size=12, color='#94a3b8', family='IBM Plex Mono')),
        legend=dict(bgcolor='#fff', bordercolor='#e2e8f0', borderwidth=1, font=dict(color='#64748b')),
        height=400, margin=dict(t=45, b=40, l=55, r=15),
        font=dict(family='IBM Plex Sans')
    )
    fig_f = None
    if fi:
        renamed = {FEAT_LABELS.get(k, k): v for k, v in fi.items()}
        df_fi = pd.DataFrame({'F': list(renamed.keys()), 'I': list(renamed.values())}).sort_values('I')
        fig_f = go.Figure(go.Bar(
            x=df_fi['I'], y=df_fi['F'], orientation='h',
            marker=dict(color=df_fi['I'],
                        colorscale=[[0,'#e2e8f0'],[0.5,'#2563eb'],[1,'#7c3aed']],
                        showscale=False)
        ))
        fig_f.update_layout(
            paper_bgcolor='#fff', plot_bgcolor='#f8fafc',
            xaxis=dict(title='Importance Score', gridcolor='#f1f5f9',
                       tickfont=dict(family='IBM Plex Mono', size=11, color='#94a3b8')),
            yaxis=dict(tickfont=dict(family='IBM Plex Sans', size=11, color='#334155')),
            height=480, margin=dict(t=15, b=40, l=220, r=15),
            font=dict(family='IBM Plex Sans')
        )
    return fig_s, fig_f

fig_scatter, fig_fi_chart = static_charts()

# ── Fungsi Prediksi ───────────────────────────────────────────────────────────
def predict(_model, _features, store_id, day_of_week, promo, state_holiday,
            school_holiday, store_type, assortment, comp_dist,
            comp_month, comp_year, promo2, p2_week, p2_year,
            promo_interval, year, month, day, week):
    row = pd.DataFrame([{
        'Store': store_id, 'DayOfWeek': day_of_week, 'Promo': promo,
        'StateHoliday': state_holiday, 'SchoolHoliday': school_holiday,
        'StoreType': store_type, 'Assortment': assortment,
        'CompetitionDistance': comp_dist,
        'CompetitionOpenSinceMonth': comp_month, 'CompetitionOpenSinceYear': comp_year,
        'Promo2': promo2, 'Promo2SinceWeek': p2_week, 'Promo2SinceYear': p2_year,
        'PromoInterval': promo_interval,
        'Year': year, 'Month': month, 'Day': day, 'WeekOfYear': week
    }])[_features]

    pred_raw = np.expm1(_model.predict(row)[0])
    pred_idr = pred_raw * EUR_TO_IDR

    try:
        all_preds = np.expm1(
            np.column_stack([t.predict(row.values) for t in _model.estimators_]).ravel()
        ) * EUR_TO_IDR
        std  = np.std(all_preds)
        conf = float(np.clip(100.0 - (std / pred_idr * 100), 40, 99.9)) if pred_idr > 0 else 60.0
        lo   = float(max(0, pred_idr - 1.96 * std))
        hi   = float(pred_idr + 1.96 * std)
    except Exception:
        conf = ev['r2'] * 100
        lo   = pred_idr - ev['mae'] * EUR_TO_IDR
        hi   = pred_idr + ev['mae'] * EUR_TO_IDR

    return float(pred_idr), conf, lo, hi

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar.form("inputs"):

    st.markdown("**Profil Toko**")

    # Ukuran Toko (menggantikan StoreType a/b/c/d)
    st_type = st.selectbox(
        "Ukuran Toko",
        [("Kecil — Minimarket / Convenience Store", 0),
         ("Besar — Supermarket / Department Store", 1),
         ("Spesialis — Fokus Satu Kategori Produk", 2),
         ("Sangat Besar — Hypermarket / Mall Anchor", 3)],
        format_func=lambda x: x[0],
        help="Pilih format yang paling sesuai dengan toko Anda."
    )

    # Ragam Produk (menggantikan Assortment a/b/c)
    asst = st.selectbox(
        "Ragam Produk",
        [("Basic — Hanya produk kebutuhan inti", 0),
         ("Standard — Inti + beberapa kategori tambahan", 1),
         ("Lengkap — Semua kategori tersedia", 2)],
        format_func=lambda x: x[0],
        help="Seberapa luas jangkauan produk toko Anda?"
    )

    # Estimasi pengunjung harian (digunakan sebagai Store ID internal)
    footfall = st.slider(
        "Estimasi Pengunjung Harian",
        min_value=50, max_value=5000, value=500, step=50,
        help="Perkiraan jumlah pelanggan yang mengunjungi toko per hari. "
             "Nilai ini digunakan sebagai proxy profil toko."
    )
    # Petakan footfall ke range Store ID (1–1115)
    store_id = max(1, min(1115, int(footfall / 5000 * 1114) + 1))

    st.markdown("**Tanggal Transaksi**")
    sel_date = st.date_input("Tanggal", value=date.today())

    st.markdown("**Promosi**")
    promo = st.radio(
        "Sedang Ada Promosi?",
        [("Ya", 1), ("Tidak", 0)],
        format_func=lambda x: x[0], horizontal=True,
        help="Apakah ada diskon, kampanye, atau event penjualan hari ini?"
    )
    promo2 = st.radio(
        "Program Loyalitas / Member?",
        [("Ya", 1), ("Tidak", 0)],
        format_func=lambda x: x[0], horizontal=True,
        help="Program promosi berulang untuk pelanggan setia atau anggota."
    )
    p_int = st.selectbox(
        "Periode Aktif Promo Member",
        [("Tidak Ada", 0),
         ("Jan / Apr / Jul / Okt", 1),
         ("Feb / Mei / Agu / Nov", 2),
         ("Mar / Jun / Sep / Des", 3)],
        format_func=lambda x: x[0],
        help="Bulan-bulan mana program loyalitas biasanya aktif?"
    )
    p2w = st.number_input("Mulai Promo Member — Minggu ke- (0 = N/A)", 0, 52, 0)
    p2y = st.number_input("Mulai Promo Member — Tahun (0 = N/A)", 0, 2025, 0)

    st.markdown("**Hari Libur**")
    s_hol = st.selectbox(
        "Jenis Hari Libur",
        [("Hari Biasa", 0),
         ("Hari Libur Nasional (Harnas, dll.)", 1),
         ("Hari Raya Besar (Lebaran / Idul Fitri)", 2),
         ("Natal / Tahun Baru", 3)],
        format_func=lambda x: x[0],
        help="Apakah tanggal yang dipilih merupakan hari libur?"
    )
    sc_hol = st.radio(
        "Libur Sekolah?",
        [("Ya", 1), ("Tidak", 0)],
        format_func=lambda x: x[0], horizontal=True,
        help="Apakah sekolah sedang libur semester?"
    )

    st.markdown("**Pesaing Terdekat**")
    comp_dist = st.number_input(
        "Jarak ke Pesaing Terdekat (meter)", 0, 100000, 1000, 100,
        help="Jarak kira-kira ke toko pesaing terdekat."
    )
    comp_month = st.selectbox(
        "Pesaing Mulai Buka — Bulan (0 = tidak diketahui)",
        list(range(0, 13)), index=0
    )
    comp_year = st.number_input(
        "Pesaing Mulai Buka — Tahun (0 = tidak diketahui)", 0, 2025, 0
    )

    run = st.form_submit_button("Jalankan Simulasi", use_container_width=True)

# ── Proses Submit ─────────────────────────────────────────────────────────────
if run:
    dow = sel_date.weekday() + 1
    woy = sel_date.isocalendar()[1]
    pred, conf, lo, hi = predict(
        model, FEATURES, store_id, dow, promo[1], s_hol[1], sc_hol[1],
        st_type[1], asst[1], comp_dist, comp_month, comp_year,
        promo2[1], p2w, p2y, p_int[1],
        sel_date.year, sel_date.month, sel_date.day, woy
    )
    st.session_state.res = dict(
        pred=pred, conf=conf, lo=lo, hi=hi,
        footfall=footfall, date=sel_date, dow=dow,
        promo=promo, st_type=st_type, asst=asst,
        s_hol=s_hol, comp_dist=comp_dist
    )

# ── Konten Utama ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.title("Simulasi Penjualan Ritel")

if 'res' not in st.session_state:
    st.markdown(
        '<p style="color:#94a3b8;font-size:.9rem;">'
        'Atur parameter toko di sidebar kiri, lalu klik <strong>Jalankan Simulasi</strong> '
        'untuk mendapatkan estimasi penjualan harian.</p>',
        unsafe_allow_html=True
    )
else:
    r = st.session_state.res

    size_label = r["st_type"][0].split(" — ")[0]
    asst_label = r["asst"][0].split(" — ")[0]
    hol_label  = r["s_hol"][0].split(" (")[0] if r["s_hol"][1] else "Hari Biasa"
    day_names  = ["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
    day_label  = day_names[r["dow"] - 1]

    st.markdown(
        f'<p style="color:#94a3b8;font-size:.82rem;margin-top:-8px;">'
        f'{size_label} &nbsp;·&nbsp; ~{r["footfall"]:,} pengunjung/hari &nbsp;·&nbsp; {r["date"].strftime("%d %b %Y")}</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Pills ringkasan skenario
    st.markdown(
        f'<span class="pill">{size_label}</span>'
        f'<span class="pill">{asst_label}</span>'
        f'<span class="pill">{day_label}</span>'
        f'<span class="pill">Promo {"Aktif" if r["promo"][1] else "Tidak Aktif"}</span>'
        f'<span class="pill">{hol_label}</span>'
        f'<span class="pill">{r["comp_dist"]:,} m ke pesaing</span>'
        f'<span class="pill">~{r["footfall"]:,} pengunjung/hari</span>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col_hero, col_status = st.columns([1.5, 1])

    with col_hero:
        st.markdown(
            f'<div class="hero-card">'
            f'<div class="hero-eyebrow">Estimasi Penjualan Harian</div>'
            f'<div class="hero-amount">Rp {r["pred"]:,.0f}</div>'
            f'<div class="hero-model">{ev["model_name"]}</div>'
            f'<div class="conf-row" style="margin-top:16px;">'
            f'<span class="conf-label">Kepercayaan</span>'
            f'<div class="conf-track"><div class="conf-fill" style="width:{r["conf"]}%"></div></div>'
            f'<span class="conf-pct">{r["conf"]:.1f}%</span>'
            f'</div>'
            f'<div class="hero-stats">'
            f'<div class="hero-stat"><div class="hero-stat-label">Batas Bawah 95%</div><div class="hero-stat-value">Rp {r["lo"]:,.0f}</div></div>'
            f'<div class="hero-stat"><div class="hero-stat-label">Batas Atas 95%</div><div class="hero-stat-value">Rp {r["hi"]:,.0f}</div></div>'
            f'<div class="hero-stat center"><div class="hero-stat-label">Confidence</div><div class="hero-stat-value">{r["conf"]:.1f}%</div></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col_status:
        if r['pred'] >= 175_000_000:
            cls, badge, title, body = (
                'high', 'Penjualan Tinggi', 'Hari Performa Kuat',
                'Prediksi di atas rata-rata. Pastikan stok dan jumlah staf memadai untuk menghadapi lonjakan permintaan.'
            )
        elif r['pred'] >= 87_500_000:
            cls, badge, title, body = (
                'mid', 'Sedang', 'Hari Penjualan Normal',
                'Performa dalam kisaran wajar. Pertimbangkan mengaktifkan promosi untuk mendorong pendapatan lebih tinggi.'
            )
        else:
            cls, badge, title, body = (
                'low', 'Penjualan Rendah', 'Hari di Bawah Rata-rata',
                'Prediksi lemah. Tinjau strategi promosi, jumlah staf, dan perencanaan inventaris untuk menekan biaya idle.'
            )
        st.markdown(
            f'<div class="status-kpi status-{cls}">'
            f'<span class="status-badge">{badge}</span>'
            f'<div class="status-title-text">{title}</div>'
            f'<div class="status-body">{body}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:.65rem;">Faktor Paling Berpengaruh</div>', unsafe_allow_html=True)
        if fi:
            renamed_fi = {FEAT_LABELS.get(k, k): v for k, v in fi.items()}
            max_score = max(renamed_fi.values())
            for feat in list(renamed_fi.keys())[:4]:
                score = renamed_fi[feat]
                w = int(score / max_score * 100)
                st.markdown(
                    f'<div class="fi-row">'
                    f'<div class="fi-label"><span>{feat}</span><span class="fi-score">{score:.4f}</span></div>'
                    f'<div class="fi-track"><div class="fi-fill" style="width:{w}%"></div></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# ── Evaluasi Model ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">Evaluasi Model</div>', unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)
mae_ok  = ev['mae_pct']  < 15
rmse_ok = ev['rmse_pct'] < 15
r2_ok   = ev['r2'] > 0.85

e1.markdown(
    f'<div class="eval-card model">'
    f'<div class="eval-eyebrow">Model</div>'
    f'<div class="eval-value" style="font-size:1.1rem;font-family:\'IBM Plex Sans\',sans-serif;">{ev["model_name"]}</div>'
    f'</div>', unsafe_allow_html=True)

e2.markdown(
    f'<div class="eval-card mae">'
    f'<div class="eval-eyebrow">MAE</div>'
    f'<div class="eval-value" style="font-size:1.1rem;">Rp {ev["mae"] * EUR_TO_IDR:,.0f}</div>'
    f'<span class="eval-delta {"ok" if mae_ok else "warn"}">↑ {ev["mae_pct"]:.2f}% dari rata-rata</span>'
    f'</div>', unsafe_allow_html=True)

e3.markdown(
    f'<div class="eval-card rmse">'
    f'<div class="eval-eyebrow">RMSE</div>'
    f'<div class="eval-value" style="font-size:1.1rem;">Rp {ev["rmse"] * EUR_TO_IDR:,.0f}</div>'
    f'<span class="eval-delta {"ok" if rmse_ok else "warn"}">↑ {ev["rmse_pct"]:.2f}% dari rata-rata</span>'
    f'</div>', unsafe_allow_html=True)

e4.markdown(
    f'<div class="eval-card r2">'
    f'<div class="eval-eyebrow">R²</div>'
    f'<div class="eval-value">{ev["r2"]:.4f}</div>'
    f'<span class="eval-delta {"ok" if r2_ok else "warn"}">{"✓ Melebihi 0.85" if r2_ok else "✗ Di bawah 0.85"}</span>'
    f'</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
for col, label, val, ok in [
    (t1, "MAE < 15%",  f"{ev['mae_pct']:.2f}%",  mae_ok),
    (t2, "RMSE < 15%", f"{ev['rmse_pct']:.2f}%", rmse_ok),
    (t3, "R² > 0.85",  f"{ev['r2']:.4f}",        r2_ok),
]:
    clr = '#10b981' if ok else '#ef4444'
    col.markdown(
        f'<div class="threshold-strip"><div class="trow">'
        f'<span class="dp" style="background:{clr}"></span>'
        f'<span style="font-weight:500;color:#334155">{label}</span>'
        f'<span style="margin-left:auto;font-family:IBM Plex Mono,monospace;color:#0f172a;font-weight:600">{val}</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Aktual vs Prediksi (Evaluasi Training)</div>', unsafe_allow_html=True)
st.plotly_chart(fig_scatter, use_container_width=True)

if fig_fi_chart:
    st.markdown('<div class="section-title">Faktor yang Mempengaruhi Prediksi</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_fi_chart, use_container_width=True)

st.markdown("---")
st.markdown(
    '<p style="font-size:.76rem;color:#94a3b8;">'
    'Kelompok 1 — LM01 &nbsp;·&nbsp; Louis Huang &nbsp;·&nbsp; '
    'Gilbert Tjandra Adanarianto &nbsp;·&nbsp; Dava Rabbani Adrian Widyatmoko<br>'
    'Model dilatih menggunakan dataset '
    '<a href="https://www.kaggle.com/datasets/shahpranshu27/rossman-store-sales" style="color:#94a3b8">'
    'Rossman Store Sales</a> — pola penjualan ritel digeneralisasi untuk simulasi bisnis.</p>',
    unsafe_allow_html=True
)