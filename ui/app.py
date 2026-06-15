import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st

st.set_page_config(
    page_title="SalesBot Analytics",
    page_icon="\U0001f4ca",
    layout="wide"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .stApp {
    background-color: #0a1120 !important;
    color: #e2e8f0 !important;
}
.block-container { padding: 3rem 4rem !important; max-width: 1100px !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 2rem 0;
background:radial-gradient(ellipse at 50% 0%,#1e3a5f 0%,transparent 70%);">
<div style="width:72px;height:72px;background:linear-gradient(135deg,#3b82f6,#6366f1);
border-radius:20px;display:inline-flex;align-items:center;justify-content:center;
font-size:2rem;margin-bottom:1.5rem;box-shadow:0 0 40px rgba(59,130,246,0.3);">\U0001f4ca</div>
<br>
<span style="color:#f1f5f9;font-size:2.8rem;font-weight:800;letter-spacing:-0.02em;">
SalesBot </span><span style="color:#3b82f6;font-size:2.8rem;font-weight:800;">Analytics</span>
<p style="color:#64748b;font-size:1.05rem;margin:1rem 0 2rem 0;line-height:1.7;">
Platform analitik penjualan retail berbasis AI.<br>
Data real-time &middot; Insight otomatis &middot; AI Agent.
</p>
<a href="/Dashboard" target="_self" style="background:#3b82f6;color:white;padding:0.7rem 1.8rem;
border-radius:10px;text-decoration:none;font-weight:600;font-size:0.95rem;margin-right:0.75rem;">
\U0001f4ca Buka Dashboard</a>
<a href="/SalesBot" target="_self" style="background:#1e293b;color:#cbd5e1;padding:0.7rem 1.8rem;
border-radius:10px;text-decoration:none;font-weight:600;font-size:0.95rem;
border:1px solid #334155;">\U0001f916 SalesBot AI</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
<div style="background:#111827;border:1px solid #1e293b;border-radius:16px;padding:1.8rem;height:100%;">
<div style="width:44px;height:44px;background:linear-gradient(135deg,#1e3a5f,#1e293b);
border-radius:10px;display:inline-flex;align-items:center;justify-content:center;
font-size:1.3rem;margin-bottom:1rem;border:1px solid #334155;">\U0001f4c8</div>
<h3 style="color:#f1f5f9;margin:0 0 0.5rem 0;font-size:1.05rem;font-weight:600;">Dashboard Analytics</h3>
<p style="color:#475569;font-size:0.875rem;line-height:1.7;margin:0 0 1rem 0;">
Visualisasi revenue, profit, dan unit terjual per provinsi, kategori, dan produk dengan filter interaktif.
</p>
<p style="color:#64748b;font-size:0.82rem;line-height:2;margin:0;">
\U0001f539 KPI cards dengan delta perbandingan<br>
\U0001f539 Revenue by province &amp; category<br>
\U0001f539 Monthly trend &amp; drill-down harian<br>
\U0001f539 Top products &amp; province ranking
</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:#111827;border:1px solid #1e293b;border-radius:16px;padding:1.8rem;height:100%;">
<div style="width:44px;height:44px;background:linear-gradient(135deg,#312e81,#1e293b);
border-radius:10px;display:inline-flex;align-items:center;justify-content:center;
font-size:1.3rem;margin-bottom:1rem;border:1px solid #334155;">\U0001f916</div>
<h3 style="color:#f1f5f9;margin:0 0 0.5rem 0;font-size:1.05rem;font-weight:600;">SalesBot AI Assistant</h3>
<p style="color:#475569;font-size:0.875rem;line-height:1.7;margin:0 0 1rem 0;">
Tanyakan pertanyaan bisnis dalam bahasa natural. AI Agent menganalisis data Supabase secara real-time.
</p>
<p style="color:#64748b;font-size:0.82rem;line-height:2;margin:0;">
\U0001f539 Analisis produk, provinsi &amp; kategori<br>
\U0001f539 Analisis metode pembayaran<br>
\U0001f539 Tren penjualan &amp; rekomendasi bisnis<br>
\U0001f539 Riwayat percakapan tersimpan
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, icon, val, label in [
    (c1, "\U0001f4cd", "6",    "Provinsi"),
    (c2, "\U0001f3f7\ufe0f",  "7",    "Kategori Produk"),
    (c3, "\U0001f4c5", "2",    "Tahun Data"),
    (c4, "\U0001f7e2", "Live", "Koneksi Supabase"),
]:
    with col:
        st.markdown(
            f"<div style='background:#111827;border:1px solid #1e293b;border-radius:12px;"
            f"padding:1.2rem;text-align:center;'>"
            f"<p style='font-size:1.5rem;margin:0;'>{icon}</p>"
            f"<p style='color:#f1f5f9;font-size:1.5rem;font-weight:700;margin:0.3rem 0 0.2rem 0;'>{val}</p>"
            f"<p style='color:#475569;font-size:0.78rem;margin:0;'>{label}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

st.markdown("""
<p style="color:#1e3a5f;font-size:0.78rem;text-align:center;margin-top:2rem;">
Celerates Final Project &middot; Kelompok 8
</p>
""", unsafe_allow_html=True)