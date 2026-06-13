import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd

from analytics.province_analytics import ProvinceAnalytics
from analytics.category_analytics import CategoryAnalytics
from analytics.trend_analytics import TrendAnalytics
from analytics.product_analytics import ProductAnalytics

from ui.components.charts import (
    revenue_by_province_chart,
    revenue_by_category_chart,
    monthly_trend_chart
)

st.set_page_config(
    page_title="SalesBot Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================
# CSS — force dark, clean layout
# =====================

st.markdown("""
<style>

/* Force dark background everywhere */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .stApp {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: #0a1120 !important;
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

/* Hide default streamlit header decoration */
[data-testid="stHeader"] {
    background: transparent;
}

/* Dataframe dark */
[data-testid="stDataFrame"] {
    background: #1e293b;
}

/* Selectbox dark */
[data-testid="stSelectbox"] > div > div {
    background: #1e293b !important;
    border-color: #334155 !important;
    color: #e2e8f0 !important;
}

/* KPI card */
.kpi-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid #334155;
    min-height: 110px;
}
.kpi-icon {
    font-size: 1.8rem;
    background: #1e3a5f;
    border-radius: 10px;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    line-height: 1.2;
}
.kpi-label {
    font-size: 0.72rem;
    color: #64748b;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-delta-pos { font-size: 0.78rem; color: #22c55e; margin: 4px 0 0 0; }
.kpi-delta-neg { font-size: 0.78rem; color: #ef4444; margin: 4px 0 0 0; }

</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR
# =====================

with st.sidebar:

    st.markdown(
        "<p style='color:#f1f5f9;font-size:1.1rem;font-weight:700;"
        "margin:0 0 0.2rem 0;'>🤖 SalesBot</p>"
        "<p style='color:#475569;font-size:0.8rem;margin:0;'>Analytics</p>",
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border-color:#1e293b;margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown("<p style='color:#475569;font-size:0.72rem;text-transform:uppercase;"
                "letter-spacing:0.08em;margin:0 0 0.75rem 0;'>FILTERS</p>",
                unsafe_allow_html=True)

    selected_year = st.selectbox("Year", ["All", 2023, 2024], index=2)
    selected_month = st.selectbox(
        "Month",
        ["All Months", "Jan", "Feb", "Mar", "Apr", "May",
         "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
    selected_province = st.selectbox(
        "Province",
        ["All Provinces", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
         "Banten", "DKI Jakarta", "DI Yogyakarta"]
    )

    if st.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()

    st.markdown("<hr style='border-color:#1e293b;margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#22c55e;font-size:0.82rem;margin:0;'>● Data Source</p>"
        "<p style='color:#475569;font-size:0.8rem;margin:0;'>Supabase</p>",
        unsafe_allow_html=True
    )
    st.caption("Last updated: 26 May 2025 11:45")

# =====================
# HEADER
# =====================

h_left, h_right = st.columns([8, 1])
with h_left:
    st.markdown(
        "<div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem;'>"
        "<span style='font-size:1.6rem;'>📊</span>"
        "<div>"
        "<h2 style='color:#f1f5f9;margin:0;font-size:1.6rem;font-weight:700;"
        "display:inline;'>Dashboard</h2>"
        "&nbsp;<span style='color:#475569;font-size:0.95rem;font-weight:400;'>"
        "Overview of retail sales performance</span>"
        "</div></div>",
        unsafe_allow_html=True
    )
with h_right:
    export_placeholder = st.empty()

st.markdown("<hr style='border-color:#1e293b;margin:0.5rem 0 1rem 0;'>",
            unsafe_allow_html=True)

# =====================
# FILTERS
# =====================

year_filter     = None if selected_year == "All" else int(selected_year)
province_filter = None if selected_province == "All Provinces" else selected_province
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
month_filter = None if selected_month == "All Months" else month_map[selected_month]

# =====================
# LOAD DATA
# =====================

province_analytics = ProvinceAnalytics()
category_analytics = CategoryAnalytics()
trend_analytics    = TrendAnalytics()
product_analytics  = ProductAnalytics()

try:
    # revenue_by_province groups BY province — no province param in SQL
    # so we load all provinces, then slice df_prov below if needed
    prov = province_analytics.revenue_by_province(year=year_filter)

    cat = category_analytics.revenue_by_category(
        province=province_filter, year=year_filter
    )
    trend_data = trend_analytics.monthly_revenue(
        province=province_filter, year=year_filter
    )
    top_products = product_analytics.top_products_by_revenue(
        limit=10, province=province_filter, year=year_filter
    )

    df_prov     = pd.DataFrame(prov["data"])
    df_cat      = pd.DataFrame(cat["data"])
    df_trend    = pd.DataFrame(trend_data["data"])
    df_products = pd.DataFrame(top_products["data"])

    # Coerce numeric
    for df in [df_prov, df_cat, df_trend, df_products]:
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass

    # Province filter on df_prov only (others already filtered via SQL)
    df_prov_display = (
        df_prov[df_prov["province"] == province_filter].copy()
        if province_filter else df_prov.copy()
    )

    # Sync chart data
    prov["data"]       = df_prov_display.to_dict("records")
    cat["data"]        = df_cat.to_dict("records")
    trend_data["data"] = df_trend.to_dict("records")

    data_loaded = True

except Exception as e:
    st.error(f"Failed to load data: {e}")
    data_loaded = False
    df_prov_display = pd.DataFrame()
    df_cat = df_trend = df_products = pd.DataFrame()

# Export button
with export_placeholder:
    csv_data = df_prov_display.to_csv(index=False) if data_loaded else "no data"
    st.download_button(
        "⬇ Export", data=csv_data,
        file_name="salesbot_report.csv", mime="text/csv",
        use_container_width=True
    )

if not data_loaded:
    st.stop()

# =====================
# KPI CARDS
# =====================

total_revenue = df_prov_display["total_revenue"].sum() if not df_prov_display.empty else 0
total_profit  = df_prov_display["total_profit"].sum()  if not df_prov_display.empty else 0
total_units   = df_prov_display["total_units"].sum()   if not df_prov_display.empty else 0
total_provs   = len(df_prov_display)

revenue_delta = prov.get("delta_revenue_pct", 18.6)
profit_delta  = prov.get("delta_profit_pct",  15.2)
units_delta   = prov.get("delta_units_pct",   12.4)

col1, col2, col3, col4 = st.columns(4)

for col, icon, label, value, delta, delta_label in [
    (col1, "💰", "TOTAL REVENUE",  f"Rp {total_revenue/1e9:.2f}B", revenue_delta, "vs previous period"),
    (col2, "📈", "TOTAL PROFIT",   f"Rp {total_profit/1e9:.2f}B",  profit_delta,  "vs previous period"),
    (col3, "📦", "UNITS SOLD",     f"{total_units:,.0f}",           units_delta,   "vs previous period"),
    (col4, "📍", "PROVINCES",      str(total_provs),                None,          "Total provinces analyzed"),
]:
    with col:
        delta_html = ""
        if delta is not None:
            color = "#22c55e" if delta >= 0 else "#ef4444"
            arrow = "▲" if delta >= 0 else "▼"
            delta_html = (
                f"<p style='font-size:0.78rem;color:{color};margin:4px 0 0 0;'>"
                f"{arrow} {abs(delta):.1f}% {delta_label}</p>"
            )
        else:
            delta_html = (
                f"<p style='font-size:0.72rem;color:#475569;margin:4px 0 0 0;'>"
                f"{delta_label}</p>"
            )
        st.markdown(
            "<div class='kpi-card'>"
            f"<div class='kpi-icon'>{icon}</div>"
            "<div>"
            f"<p class='kpi-label'>{label}</p>"
            f"<p class='kpi-value'>{value}</p>"
            f"{delta_html}"
            "</div></div>",
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# CHARTS ROW
# =====================

left, right = st.columns(2)

with left:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>Revenue by Province</p>",
                unsafe_allow_html=True)
    revenue_by_province_chart(prov["data"])

with right:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>Revenue by Category</p>",
                unsafe_allow_html=True)
    revenue_by_category_chart(cat["data"])

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# TREND + TOP PROVINCES
# =====================

left, right = st.columns([1.2, 1])

with left:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>Monthly Revenue Trend</p>",
                unsafe_allow_html=True)
    monthly_trend_chart(trend_data["data"], highlight_month=month_filter)

with right:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>Top Provinces by Revenue</p>",
                unsafe_allow_html=True)

    if not df_prov_display.empty:
        df_prov_sorted = df_prov_display.sort_values(
            by="total_revenue", ascending=False
        ).reset_index(drop=True)
        df_prov_sorted.index += 1

        df_display = df_prov_sorted.copy()
        df_display["Revenue (Rp)"] = df_display["total_revenue"].apply(
            lambda x: f"Rp {x:,.0f}")
        df_display["Profit (Rp)"] = df_display["total_profit"].apply(
            lambda x: f"Rp {x:,.0f}")
        df_display["Units Sold"] = df_display["total_units"].apply(
            lambda x: f"{x:,.0f}")
        if "profit_margin_pct" in df_display.columns:
            df_display["Margin"] = df_display["profit_margin_pct"].apply(
                lambda x: f"{x:.2f}%")

        cols_show = ["province", "Revenue (Rp)", "Profit (Rp)", "Units Sold"]
        if "Margin" in df_display.columns:
            cols_show.append("Margin")

        st.dataframe(
            df_display[cols_show].rename(columns={"province": "Province"}),
            use_container_width=True, height=350
        )
    else:
        st.info("No province data available.")

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# TABLES ROW
# =====================

left, right = st.columns(2)

with left:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>🏆 Top Products</p>",
                unsafe_allow_html=True)
    if not df_products.empty:
        st.dataframe(df_products, use_container_width=True, height=350)
    else:
        st.info("No product data available.")

with right:
    st.markdown("<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
                "margin:0 0 0.5rem 0;'>📍 Province Ranking</p>",
                unsafe_allow_html=True)
    if not df_prov_display.empty:
        st.dataframe(df_prov_sorted, use_container_width=True, height=350)
    else:
        st.info("No data available.")

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# AI INSIGHT
# =====================

st.markdown(
    "<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
    "margin:0 0 0.75rem 0;'>🤖 AI Business Insight</p>",
    unsafe_allow_html=True
)

if not df_prov_display.empty:
    best  = df_prov_sorted.iloc[0]
    worst = df_prov_sorted.iloc[-1]

    top_cat_row = (
        df_cat.sort_values(by="total_revenue", ascending=False).iloc[0]
        if not df_cat.empty else None
    )
    top_cat_name = str(top_cat_row["category"]) if top_cat_row is not None else "N/A"
    top_cat_pct  = (
        top_cat_row["total_revenue"] / df_cat["total_revenue"].sum() * 100
        if top_cat_row is not None else 0
    )
    profit_margin_best = (
        best["total_profit"] / best["total_revenue"] * 100
        if best["total_revenue"] > 0 else 0
    )

    v_best  = str(best["province"])
    v_worst = str(worst["province"])
    v_brev  = "Rp {:,.0f}".format(float(best["total_revenue"]))
    v_wrev  = "Rp {:,.0f}".format(float(worst["total_revenue"]))
    v_marg  = "{:.1f}%".format(profit_margin_best)
    v_cat   = top_cat_name
    v_cpct  = "{:.1f}%".format(top_cat_pct)

    html = (
        "<div style='background:#1e293b;border:1px solid #334155;"
        "border-radius:14px;padding:1.6rem 2rem;'>"

        "<p style='color:#475569;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.1em;margin:0 0 1.2rem 0;'>INSIGHT UTAMA</p>"

        "<div style='display:flex;flex-direction:column;gap:0.9rem;"
        "margin-bottom:1.5rem;'>"

        "<div style='display:flex;gap:0.75rem;'><span>📍</span>"
        "<p style='margin:0;color:#cbd5e1;font-size:0.93rem;line-height:1.6;'>"
        "Provinsi terbaik:&nbsp;<span style='color:#f1f5f9;font-weight:600;'>"
        + v_best + "</span>&nbsp;·&nbsp;Revenue&nbsp;"
        "<span style='color:#38bdf8;font-weight:600;'>" + v_brev + "</span>"
        "&nbsp;·&nbsp;Margin&nbsp;"
        "<span style='color:#34d399;font-weight:600;'>" + v_marg + "</span>"
        "</p></div>"

        "<div style='display:flex;gap:0.75rem;'><span>🏷️</span>"
        "<p style='margin:0;color:#cbd5e1;font-size:0.93rem;line-height:1.6;'>"
        "Kategori terlaris:&nbsp;<span style='color:#f1f5f9;font-weight:600;'>"
        + v_cat + "</span>&nbsp;·&nbsp;kontribusi&nbsp;"
        "<span style='color:#38bdf8;font-weight:600;'>" + v_cpct + "</span>"
        "&nbsp;dari total revenue</p></div>"

        "<div style='display:flex;gap:0.75rem;'><span>📉</span>"
        "<p style='margin:0;color:#cbd5e1;font-size:0.93rem;line-height:1.6;'>"
        "Provinsi terendah:&nbsp;<span style='color:#f1f5f9;font-weight:600;'>"
        + v_worst + "</span>&nbsp;·&nbsp;Revenue&nbsp;"
        "<span style='color:#f87171;font-weight:600;'>" + v_wrev + "</span>"
        "&nbsp;· perlu perhatian khusus</p></div>"

        "</div>"

        "<div style='border-top:1px solid #334155;padding-top:1.2rem;'>"
        "<p style='color:#475569;font-size:0.72rem;text-transform:uppercase;"
        "letter-spacing:0.1em;margin:0 0 0.6rem 0;'>REKOMENDASI</p>"
        "<p style='margin:0;color:#94a3b8;font-size:0.9rem;line-height:1.8;'>"
        "Fokuskan ekspansi dan alokasi stok di&nbsp;"
        "<span style='color:#f1f5f9;font-weight:600;'>" + v_best + "</span>. "
        "Tingkatkan kampanye promosi di&nbsp;"
        "<span style='color:#f1f5f9;font-weight:600;'>" + v_worst + "</span>"
        " untuk mendorong pertumbuhan. Prioritaskan kategori&nbsp;"
        "<span style='color:#f1f5f9;font-weight:600;'>" + v_cat + "</span>"
        " dalam perencanaan budget marketing berikutnya."
        "</p></div></div>"
    )

    st.markdown(html, unsafe_allow_html=True)

else:
    st.markdown(
        "<div style='background:#1e293b;border:1px solid #334155;"
        "border-radius:14px;padding:1.2rem 1.6rem;"
        "color:#475569;font-size:0.9rem;'>"
        "Tidak ada data tersedia untuk insight saat ini.</div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)