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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .stApp {
    background-color: #060d1a !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.block-container { padding: 0 3rem 3rem 3rem !important; max-width: 1000px !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(148,163,184,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148,163,184,0.04) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
    z-index: 0;
}

body::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 50% -5%, rgba(59,130,246,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 15%, rgba(124,58,237,0.09) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 8% 75%, rgba(99,102,241,0.07) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
}

.feature-card { transition: transform 0.2s ease, box-shadow 0.25s ease, border-color 0.25s ease; }
.feature-card:hover { transform: translateY(-4px); }
.cta-btn:hover { opacity: 0.88; transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

LOGO_SVG = """
<svg width="82" height="82" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="lgMain" x1="0" y1="0" x2="52" y2="52" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="50%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
    <filter id="glow1" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow2" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect x="4" y="7" width="46" height="46" rx="14" fill="#3b82f6" opacity="0.2" filter="url(#glow1)"/>
  <rect width="52" height="52" rx="16" fill="url(#lgMain)"/>
  <rect x="1" y="1" width="50" height="26" rx="14" fill="rgba(255,255,255,0.07)"/>
  <rect x="8" y="28" width="9" height="15" rx="2.5" fill="rgba(255,255,255,0.32)"/>
  <rect x="21.5" y="20" width="9" height="23" rx="2.5" fill="rgba(255,255,255,0.58)"/>
  <rect x="35" y="12" width="9" height="31" rx="2.5" fill="rgba(255,255,255,0.9)"/>
  <polyline points="12.5,24 26,16 39.5,9" fill="none" stroke="rgba(255,255,255,0.35)"
    stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow2)"/>
  <polyline points="12.5,24 26,16 39.5,9" fill="none" stroke="white"
    stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12.5" cy="24" r="3.2" fill="#60a5fa"/>
  <circle cx="12.5" cy="24" r="1.8" fill="white"/>
  <circle cx="26" cy="16" r="3.2" fill="#818cf8"/>
  <circle cx="26" cy="16" r="1.8" fill="white"/>
  <circle cx="39.5" cy="9" r="3.2" fill="#a78bfa"/>
  <circle cx="39.5" cy="9" r="1.8" fill="white"/>
</svg>
"""

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
padding:1.25rem 0;border-bottom:1px solid rgba(148,163,184,0.07);margin-bottom:0;">
  <div style="display:flex;align-items:center;gap:10px;">
    <svg width="34" height="34" viewBox="0 0 52 52" fill="none">
      <defs>
        <linearGradient id="lgNav" x1="0" y1="0" x2="52" y2="52" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#7c3aed"/>
        </linearGradient>
      </defs>
      <rect width="52" height="52" rx="13" fill="url(#lgNav)"/>
      <rect x="8" y="28" width="9" height="15" rx="2.5" fill="rgba(255,255,255,0.35)"/>
      <rect x="21.5" y="20" width="9" height="23" rx="2.5" fill="rgba(255,255,255,0.6)"/>
      <rect x="35" y="12" width="9" height="31" rx="2.5" fill="rgba(255,255,255,0.9)"/>
      <polyline points="12.5,24 26,16 39.5,9" fill="none" stroke="white"
        stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="12.5" cy="24" r="2.5" fill="white"/>
      <circle cx="26" cy="16" r="2.5" fill="white"/>
      <circle cx="39.5" cy="9" r="2.5" fill="white"/>
    </svg>
    <span style="font-weight:700;font-size:1rem;color:#f1f5f9;letter-spacing:-0.02em;">
      SalesBot<span style="color:#3b82f6;"> Analytics</span>
    </span>
  </div>
  <div style="display:flex;gap:8px;">
    <a href="/Dashboard" target="_self" style="background:transparent;color:#94a3b8;
      padding:0.38rem 0.9rem;border-radius:8px;text-decoration:none;font-size:0.8rem;
      font-weight:500;border:1px solid rgba(148,163,184,0.15);">Dashboard</a>
    <a href="/SalesBot" target="_self" style="background:transparent;color:#94a3b8;
      padding:0.38rem 0.9rem;border-radius:8px;text-decoration:none;font-size:0.8rem;
      font-weight:500;border:1px solid rgba(148,163,184,0.15);">SalesBot AI</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;padding:4rem 0 3rem;">
  <div style="display:inline-block;position:relative;margin-bottom:1.75rem;">
    <div style="position:absolute;inset:-14px;border-radius:26px;
      background:radial-gradient(circle,rgba(59,130,246,0.22) 0%,transparent 70%);"></div>
    {LOGO_SVG}
  </div>
  <div style="display:inline-flex;align-items:center;gap:7px;
    background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.25);
    border-radius:999px;padding:4px 14px 4px 10px;margin-bottom:1.4rem;">
    <div style="width:6px;height:6px;border-radius:50%;background:#22c55e;
      box-shadow:0 0 7px #22c55e;"></div>
    <span style="font-size:0.75rem;color:#93c5fd;font-weight:500;letter-spacing:0.04em;">
      LIVE &middot; Supabase Connected
    </span>
  </div>
  <br>
  <span style="color:#f8fafc;font-size:clamp(2.2rem,4vw,3.4rem);font-weight:800;
    letter-spacing:-0.035em;line-height:1.08;">SalesBot</span>
  <span style="font-size:clamp(2.2rem,4vw,3.4rem);font-weight:800;letter-spacing:-0.035em;
    line-height:1.08;background:linear-gradient(90deg,#60a5fa 0%,#818cf8 50%,#a78bfa 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;"> Analytics</span>
  <p style="color:#94a3b8;font-size:1rem;line-height:1.75;max-width:420px;
    margin:1rem auto 2.2rem;">
    Platform analitik penjualan retail berbasis AI.<br>
    Data real-time &middot; Insight otomatis &middot; AI Agent.
  </p>
  <a href="/Dashboard" target="_self" class="cta-btn" style="display:inline-flex;align-items:center;gap:8px;
    background:transparent;color:#93c5fd;
    padding:0.65rem 1.5rem;border-radius:11px;text-decoration:none;
    font-weight:600;font-size:0.9rem;margin-right:10px;
    border:1px solid rgba(59,130,246,0.5);">
    📊 Buka Dashboard
  </a>
  <a href="/SalesBot" target="_self" class="cta-btn" style="display:inline-flex;align-items:center;gap:8px;
    background:transparent;color:#93c5fd;padding:0.65rem 1.5rem;
    border-radius:11px;text-decoration:none;font-weight:600;font-size:0.9rem;
    border:1px solid rgba(59,130,246,0.5);">
    🤖 SalesBot AI
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(59,130,246,0.3),
rgba(124,58,237,0.3),transparent);margin:0 0 2.5rem;"></div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
<div class="feature-card" style="background:rgba(11,18,35,0.75);border:1px solid rgba(148,163,184,0.08);
  border-radius:20px;padding:1.6rem;position:relative;overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);height:100%;">
  <div style="position:absolute;top:0;left:20%;right:20%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(59,130,246,0.6),transparent);"></div>
  <div style="width:46px;height:46px;border-radius:12px;
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:1rem;box-shadow:0 4px 16px rgba(59,130,246,0.25);
    border:1px solid rgba(59,130,246,0.2);">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#93c5fd"
      stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="7" height="7" rx="1"/>
      <rect x="14" y="3" width="7" height="7" rx="1"/>
      <rect x="3" y="14" width="7" height="7" rx="1"/>
      <rect x="14" y="14" width="7" height="7" rx="1"/>
    </svg>
  </div>
  <h3 style="color:#f1f5f9;margin:0 0 0.45rem;font-size:1rem;font-weight:700;">Dashboard Analytics</h3>
  <p style="color:#475569;font-size:0.85rem;line-height:1.7;margin:0 0 1.1rem;">
    Visualisasi revenue, profit, dan unit terjual per provinsi, kategori, dan produk dengan filter interaktif.
  </p>
  <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:1.4rem;">
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#3b82f6;box-shadow:0 0 5px #3b82f6;flex-shrink:0;"></span>KPI cards dengan delta perbandingan</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#3b82f6;box-shadow:0 0 5px #3b82f6;flex-shrink:0;"></span>Revenue by province &amp; category</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#3b82f6;box-shadow:0 0 5px #3b82f6;flex-shrink:0;"></span>Monthly trend &amp; drill-down harian</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#3b82f6;box-shadow:0 0 5px #3b82f6;flex-shrink:0;"></span>Top products &amp; province ranking</div>
  </div>
  <a href="/Dashboard" target="_self" style="display:inline-flex;align-items:center;gap:6px;
    background:rgba(59,130,246,0.12);color:#93c5fd;padding:0.45rem 0.9rem;
    border-radius:8px;text-decoration:none;font-weight:600;font-size:0.8rem;
    border:1px solid rgba(59,130,246,0.2);">Buka Dashboard →</a>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature-card" style="background:rgba(11,18,35,0.75);border:1px solid rgba(148,163,184,0.08);
  border-radius:20px;padding:1.6rem;position:relative;overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);height:100%;">
  <div style="position:absolute;top:0;left:20%;right:20%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(124,58,237,0.6),transparent);"></div>
  <div style="width:46px;height:46px;border-radius:12px;
    background:linear-gradient(135deg,#4c1d95,#7c3aed);
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:1rem;box-shadow:0 4px 16px rgba(124,58,237,0.25);
    border:1px solid rgba(124,58,237,0.2);">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#c4b5fd"
      stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2a4 4 0 0 1 4 4v1h1a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-6a3 3 0 0 1 3-3h1V6a4 4 0 0 1 4-4z"/>
      <circle cx="9" cy="13" r="1" fill="#c4b5fd"/>
      <circle cx="15" cy="13" r="1" fill="#c4b5fd"/>
    </svg>
  </div>
  <h3 style="color:#f1f5f9;margin:0 0 0.45rem;font-size:1rem;font-weight:700;">SalesBot AI Assistant</h3>
  <p style="color:#475569;font-size:0.85rem;line-height:1.7;margin:0 0 1.1rem;">
    Tanyakan pertanyaan bisnis dalam bahasa natural. AI Agent menganalisis data Supabase secara real-time.
  </p>
  <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:1.4rem;">
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#7c3aed;box-shadow:0 0 5px #7c3aed;flex-shrink:0;"></span>Analisis produk, provinsi &amp; kategori</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#7c3aed;box-shadow:0 0 5px #7c3aed;flex-shrink:0;"></span>Analisis metode pembayaran</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#7c3aed;box-shadow:0 0 5px #7c3aed;flex-shrink:0;"></span>Tren penjualan &amp; rekomendasi bisnis</div>
    <div style="display:flex;align-items:center;gap:8px;color:#64748b;font-size:0.8rem;">
      <span style="width:5px;height:5px;border-radius:50%;background:#7c3aed;box-shadow:0 0 5px #7c3aed;flex-shrink:0;"></span>Riwayat percakapan tersimpan</div>
  </div>
  <a href="/SalesBot" target="_self" style="display:inline-flex;align-items:center;gap:6px;
    background:rgba(124,58,237,0.12);color:#c4b5fd;padding:0.45rem 0.9rem;
    border-radius:8px;text-decoration:none;font-weight:600;font-size:0.8rem;
    border:1px solid rgba(124,58,237,0.2);">Buka SalesBot →</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, icon, val, label in [
    (c1, "📍", "6",    "Provinsi"),
    (c2, "🏷️", "7",    "Kategori Produk"),
    (c3, "📅", "2",    "Tahun Data"),
    (c4, "🟢", "Live", "Koneksi Supabase"),
]:
    with col:
        st.markdown(
            f"<div style='background:rgba(11,18,35,0.6);border:1px solid rgba(148,163,184,0.07);"
            f"border-radius:14px;padding:1.2rem;text-align:center;'>"
            f"<p style='font-size:1.5rem;margin:0;'>{icon}</p>"
            f"<p style='color:#f1f5f9;font-size:1.5rem;font-weight:800;"
            f"letter-spacing:-0.03em;margin:0.3rem 0 0.2rem;line-height:1;'>{val}</p>"
            f"<p style='color:#475569;font-size:0.75rem;margin:0;'>{label}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

st.markdown("""
<div style="border-top:1px solid rgba(148,163,184,0.06);padding:1.5rem 0;margin-top:2rem;text-align:center;">
  <p style="color:#1e3a5f;font-size:0.75rem;margin:0;">
    Celerates Final Project &middot; Kelompok 8
  </p>
</div>
""", unsafe_allow_html=True)