import os
import json
import streamlit as st
from groq import Groq


def _get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan di .env")
    return Groq(api_key=api_key)


def generate_executive_summary(
    df_prov,
    df_cat,
    df_trend,
    df_products,
    selected_year,
    selected_month,
    selected_province,
) -> str:
    """
    Generate ringkasan bisnis menggunakan Groq LLM
    berdasarkan data aktual dari Supabase.
    """
    try:
        client = _get_groq_client()

        # ── Siapkan data ringkas untuk prompt ─────────────
        top_prov = (
            df_prov.sort_values("total_revenue", ascending=False).iloc[0]
            if not df_prov.empty else None
        )
        top_cat = (
            df_cat.sort_values("total_revenue", ascending=False).iloc[0]
            if not df_cat.empty else None
        )
        top_prod = (
            df_products.sort_values("total_revenue", ascending=False).iloc[0]
            if not df_products.empty else None
        )

        total_rev  = float(df_prov["total_revenue"].sum()) if not df_prov.empty else 0
        total_prof = float(df_prov["total_profit"].sum())  if not df_prov.empty else 0
        margin     = (total_prof / total_rev * 100) if total_rev > 0 else 0

        # Monthly trend — ambil 2 bulan terakhir untuk delta
        trend_delta = ""
        if not df_trend.empty and len(df_trend) >= 2:
            last  = float(df_trend.sort_values(["year","month"]).iloc[-1]["total_revenue"])
            prev  = float(df_trend.sort_values(["year","month"]).iloc[-2]["total_revenue"])
            delta = (last - prev) / prev * 100 if prev > 0 else 0
            trend_delta = f"{delta:+.1f}% dibanding bulan sebelumnya"

        # Province breakdown
        prov_summary = []
        if not df_prov.empty:
            total = df_prov["total_revenue"].sum()
            for _, row in df_prov.sort_values("total_revenue", ascending=False).head(3).iterrows():
                pct = row["total_revenue"] / total * 100
                prov_summary.append(
                    f"{row['province']}: Rp {float(row['total_revenue']):,.0f} ({pct:.1f}%)"
                )

        # Category breakdown
        cat_summary = []
        if not df_cat.empty:
            total = df_cat["total_revenue"].sum()
            for _, row in df_cat.sort_values("total_revenue", ascending=False).head(3).iterrows():
                pct = row["total_revenue"] / total * 100
                cat_summary.append(
                    f"{row['category']}: {pct:.1f}%"
                )

        filter_ctx = []
        if selected_year != "All":
            filter_ctx.append(f"Tahun: {selected_year}")
        if selected_month != "All Months":
            filter_ctx.append(f"Bulan: {selected_month}")
        if selected_province != "All Provinces":
            filter_ctx.append(f"Provinsi: {selected_province}")

        filter_str = ", ".join(filter_ctx) if filter_ctx else "Semua periode"

        data_context = f"""
DATA PENJUALAN RETAIL (Filter: {filter_str}):

RINGKASAN KEUANGAN:
- Total Revenue: Rp {total_rev:,.0f}
- Total Profit: Rp {total_prof:,.0f}
- Profit Margin: {margin:.1f}%
- Tren: {trend_delta or 'tidak tersedia'}

TOP 3 PROVINSI (berdasarkan revenue):
{chr(10).join(f'- {p}' for p in prov_summary) or '- Data tidak tersedia'}

TOP 3 KATEGORI (berdasarkan revenue):
{chr(10).join(f'- {c}' for c in cat_summary) or '- Data tidak tersedia'}

PRODUK TERLARIS:
- {top_prod['product_name'] if top_prod is not None else 'N/A'} 
  (Rp {float(top_prod['total_revenue']):,.0f} | Margin: {float(top_prod.get('profit_margin_pct', 0)):.1f}%)
  {"" if top_prod is None else ""}
"""

        prompt = f"""Kamu adalah analis bisnis senior yang membuat executive summary untuk manajemen.

{data_context}

Buat executive summary SINGKAT dalam Bahasa Indonesia (maksimal 5 poin bullet):
1. Kinerja revenue secara keseluruhan (naik/turun/stabil + angka)
2. Provinsi dengan kontribusi terbesar dan insight-nya
3. Kategori produk yang paling dominan
4. Produk terlaris dan potensinya
5. Satu rekomendasi strategis yang spesifik dan actionable

Format output:
- Gunakan bullet point (•)
- Setiap poin maksimal 2 kalimat
- Sertakan angka spesifik
- Bahasa profesional tapi mudah dipahami
- JANGAN tambahkan heading atau judul
- Langsung mulai dari bullet pertama"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"_Gagal generate summary: {e}_"


def render_executive_summary(
    df_prov, df_cat, df_trend, df_products,
    selected_year, selected_month, selected_province
):
    """Render executive summary card di Streamlit."""

    st.markdown(
        "<p style='color:#f1f5f9;font-size:1.1rem;font-weight:600;"
        "margin:0 0 0.75rem 0;'>🤖 Executive Summary</p>",
        unsafe_allow_html=True
    )

    # Cache key based on filters
    cache_key = f"exec_summary_{selected_year}_{selected_month}_{selected_province}"

    if cache_key not in st.session_state:
        with st.spinner("Menganalisis data bisnis..."):
            summary = generate_executive_summary(
                df_prov, df_cat, df_trend, df_products,
                selected_year, selected_month, selected_province
            )
        st.session_state[cache_key] = summary
    else:
        summary = st.session_state[cache_key]

    # Render card
    lines = [l.strip() for l in summary.split("\n") if l.strip()]
    bullets_html = "".join([
        f"<div style='display:flex;gap:0.75rem;align-items:flex-start;"
        f"margin-bottom:0.65rem;'>"
        f"<span style='color:#3b82f6;margin-top:2px;flex-shrink:0;'>•</span>"
        f"<p style='margin:0;color:#cbd5e1;font-size:0.9rem;line-height:1.6;'>"
        f"{line.lstrip('•-· ').strip()}</p></div>"
        for line in lines if line.lstrip('•-· ').strip()
    ])

    col_summary, col_btn = st.columns([8, 1])
    with col_btn:
        if st.button("↻", help="Regenerate summary", key="regen_summary"):
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            st.rerun()

    with col_summary:
        st.markdown(
            "<div style='background:#1e293b;border:1px solid #334155;"
            "border-left:3px solid #3b82f6;"
            "border-radius:12px;padding:1.2rem 1.4rem;'>"
            + bullets_html +
            "</div>",
            unsafe_allow_html=True
        )