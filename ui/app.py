import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st

st.set_page_config(
    page_title="SalesBot Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.block-container { padding-top: 2rem; }
[data-testid="stSidebar"] { background: #0f172a; }
</style>
""", unsafe_allow_html=True)

# ── Hero section ──────────────────────────────────────────

st.markdown("""
<div style="
    max-width: 820px;
    margin: 3rem auto 0 auto;
    text-align: center;
    padding: 0 1rem;
">
    <p style="font-size:3rem;margin:0;">📊</p>
    <h1 style="
        color:#f1f5f9;
        font-size:2.6rem;
        font-weight:700;
        margin:0.5rem 0 0.75rem 0;
        line-height:1.2;
    ">SalesBot Analytics</h1>
    <p style="
        color:#64748b;
        font-size:1.1rem;
        margin:0 0 2.5rem 0;
        line-height:1.6;
    ">Platform analitik penjualan retail berbasis AI.<br>
    Data real-time dari Supabase, insight otomatis dari AI Agent.</p>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
<div style="
    background:#1e293b;
    border:1px solid #334155;
    border-radius:16px;
    padding:2rem;
    height:100%;
">
    <div style="font-size:2rem;margin-bottom:1rem;">📈</div>
    <h3 style="color:#f1f5f9;margin:0 0 0.6rem 0;font-size:1.2rem;">Dashboard Analytics</h3>
    <p style="color:#64748b;margin:0 0 1.5rem 0;font-size:0.9rem;line-height:1.6;">
        Visualisasi revenue, profit, dan unit terjual per provinsi, kategori,
        dan produk. Filter interaktif berdasarkan tahun, bulan, dan wilayah.
    </p>
    <ul style="color:#94a3b8;font-size:0.88rem;padding-left:1.2rem;
               line-height:2;margin:0;">
        <li>KPI cards dengan perbandingan periode</li>
        <li>Revenue by province & category</li>
        <li>Monthly revenue trend</li>
        <li>Top products & province ranking</li>
    </ul>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="
    background:#1e293b;
    border:1px solid #334155;
    border-radius:16px;
    padding:2rem;
    height:100%;
">
    <div style="font-size:2rem;margin-bottom:1rem;">🤖</div>
    <h3 style="color:#f1f5f9;margin:0 0 0.6rem 0;font-size:1.2rem;">SalesBot AI Assistant</h3>
    <p style="color:#64748b;margin:0 0 1.5rem 0;font-size:0.9rem;line-height:1.6;">
        Tanyakan pertanyaan bisnis dalam bahasa natural.
        AI Agent menganalisis data Supabase secara real-time
        dan memberikan jawaban berbasis data aktual.
    </p>
    <ul style="color:#94a3b8;font-size:0.88rem;padding-left:1.2rem;
               line-height:2;margin:0;">
        <li>Analisis produk, provinsi & kategori</li>
        <li>Analisis metode pembayaran</li>
        <li>Tren penjualan & rekomendasi bisnis</li>
        <li>Riwayat percakapan tersimpan</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)

stats = [
    ("6", "Provinsi", "📍"),
    ("7", "Kategori Produk", "🏷️"),
    ("2", "Tahun Data", "📅"),
    ("Real-time", "Koneksi Supabase", "🟢"),
]

for col, (val, label, icon) in zip([c1, c2, c3, c4], stats):
    with col:
        st.markdown(f"""
<div style="
    background:#1e293b;
    border:1px solid #334155;
    border-radius:12px;
    padding:1.2rem;
    text-align:center;
">
    <p style="font-size:1.5rem;margin:0;">{icon}</p>
    <p style="color:#f1f5f9;font-size:1.5rem;font-weight:700;margin:0.3rem 0 0.2rem 0;">{val}</p>
    <p style="color:#64748b;font-size:0.8rem;margin:0;">{label}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center;padding:1rem 0 2rem 0;">
    <p style="color:#475569;font-size:0.85rem;">
        Gunakan menu di sidebar untuk navigasi →
        <strong style="color:#94a3b8;">Dashboard</strong> atau
        <strong style="color:#94a3b8;">SalesBot</strong>
    </p>
</div>
""", unsafe_allow_html=True)