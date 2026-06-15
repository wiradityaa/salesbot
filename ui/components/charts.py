import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =====================================
# Color palette (dark theme)
# =====================================

CHART_COLORS = [
    "#3b82f6",  # blue
    "#6366f1",  # indigo
    "#8b5cf6",  # violet
    "#ec4899",  # pink
    "#f59e0b",  # amber
    "#10b981",  # emerald
    "#f97316",  # orange
]

LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", size=12),
    margin=dict(l=0, r=0, t=10, b=0),
)


# =====================================
# Revenue by Province — Horizontal Bar
# =====================================

def revenue_by_province_chart(data):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No province data available.")
        return

    df = df.sort_values(by="total_revenue", ascending=True)

    # Shorten labels to billions
    df["label"] = df["total_revenue"].apply(
        lambda x: f"Rp {x/1e9:.1f}B"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["total_revenue"],
            y=df["province"],
            orientation="h",
            text=df["label"],
            textposition="outside",
            marker=dict(
                color=CHART_COLORS[0],
                opacity=0.9,
                line=dict(width=0)
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: Rp %{x:,.0f}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=380,
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="#1e293b",
            zeroline=False,
            tickformat=".2s",
            tickprefix="Rp "
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color="#cbd5e1")
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================
# Revenue by Category — Donut Chart
# =====================================

def revenue_by_category_chart(data):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No category data available.")
        return

    df = df.sort_values(by="total_revenue", ascending=False)

    total = df["total_revenue"].sum()

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=df["category"],
            values=df["total_revenue"],
            hole=0.55,
            textinfo="percent",
            textfont=dict(size=11),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Revenue: Rp %{value:,.0f}<br>"
                "Share: %{percent}<extra></extra>"
            ),
            marker=dict(
                colors=CHART_COLORS[:len(df)],
                line=dict(color="#0f172a", width=2)
            )
        )
    )

    # Center annotation
    fig.add_annotation(
        text=f"Rp {total/1e9:.2f}B<br><span style='font-size:10px'>Total</span>",
        x=0.5, y=0.5,
        font=dict(size=14, color="#f1f5f9"),
        showarrow=False,
        align="center"
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=380,
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.02,
            y=0.5,
            font=dict(size=11, color="#cbd5e1"),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================
# Monthly Revenue Trend — Line + Fill
# =====================================

def monthly_trend_chart(data, highlight_month: int = None, year_filter=None):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No trend data available.")
        return

    x_col = "month_name" if "month_name" in df.columns else "month"

    # ── Single month selected → bar chart ─────────────────────────────
    if len(df) == 1:
        fig = go.Figure()
        month_label = str(df.iloc[0][x_col])
        revenue_val = float(df.iloc[0]["total_revenue"])
        fig.add_trace(go.Bar(
            x=[month_label],
            y=[revenue_val],
            text=[f"Rp {revenue_val:,.0f}"],
            textposition="outside",
            marker=dict(color="#3b82f6", opacity=0.9,
                        line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Revenue: Rp %{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(
            **LAYOUT_DEFAULTS,
            height=320,
            showlegend=False,
            xaxis=dict(showgrid=False, tickfont=dict(size=13, color="#f1f5f9")),
            yaxis=dict(showgrid=True, gridcolor="#1e293b", tickformat=".2s",
                       tickprefix="Rp ", tickfont=dict(size=11, color="#94a3b8"),
                       zeroline=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        return

    fig = go.Figure()

    # ── Year = All → draw one line per year, different color ──────────
    if year_filter is None and "year" in df.columns and df["year"].nunique() > 1:

        year_colors = {
            2023: "#22c55e",   # green
            2024: "#3b82f6",   # blue
            2025: "#f59e0b",   # amber
        }

        for yr in sorted(df["year"].unique()):
            df_yr = df[df["year"] == yr].copy()

            # Marker highlight
            if highlight_month is not None and "month" in df_yr.columns:
                sizes  = [14 if int(r["month"]) == highlight_month else 5
                          for _, r in df_yr.iterrows()]
                colors = ["#facc15" if int(r["month"]) == highlight_month
                          else year_colors.get(int(yr), "#3b82f6")
                          for _, r in df_yr.iterrows()]
            else:
                sizes  = [5] * len(df_yr)
                colors = [year_colors.get(int(yr), "#3b82f6")] * len(df_yr)

            fig.add_trace(
                go.Scatter(
                    x=df_yr[x_col],
                    y=df_yr["total_revenue"],
                    mode="lines+markers",
                    name=str(int(yr)),
                    line=dict(color=year_colors.get(int(yr), "#3b82f6"),
                              width=2.5),
                    marker=dict(size=sizes, color=colors,
                                line=dict(color="#0f172a", width=1.5)),
                    hovertemplate=(
                        f"<b>%{{x}} {int(yr)}</b><br>"
                        "Revenue: Rp %{y:,.0f}<extra></extra>"
                    )
                )
            )

        fig.update_layout(
            **LAYOUT_DEFAULTS,
            height=320,
            showlegend=True,
            legend=dict(
                orientation="h", x=1, y=1.1, xanchor="right",
                font=dict(size=11, color="#94a3b8"),
                bgcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#94a3b8"),
                       zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#1e293b", tickformat=".2s",
                       tickprefix="Rp ", tickfont=dict(size=11, color="#94a3b8"),
                       zeroline=False),
            hovermode="x unified"
        )

    # ── Single year → filled area with highlight ──────────────────────
    else:
        if highlight_month is not None and "month" in df.columns:
            marker_sizes  = [14 if int(r["month"]) == highlight_month else 6
                             for _, r in df.iterrows()]
            marker_colors = ["#facc15" if int(r["month"]) == highlight_month
                             else "#3b82f6" for _, r in df.iterrows()]
        else:
            marker_sizes  = [6] * len(df)
            marker_colors = ["#3b82f6"] * len(df)

        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df["total_revenue"],
                mode="lines+markers",
                fill="tozeroy",
                fillcolor="rgba(59,130,246,0.15)",
                line=dict(color="#3b82f6", width=2.5),
                marker=dict(size=marker_sizes, color=marker_colors,
                            line=dict(color="#0f172a", width=1.5)),
                hovertemplate=(
                    "<b>%{x}</b><br>Revenue: Rp %{y:,.0f}<extra></extra>"
                )
            )
        )

        # Highlight vertical line for selected month
        if highlight_month is not None and "month" in df.columns:
            matched = df[df["month"] == highlight_month]
            if not matched.empty:
                x_label = matched.iloc[0][x_col]
                fig.add_shape(
                    type="line",
                    x0=x_label, x1=x_label,
                    y0=0, y1=1,
                    xref="x", yref="paper",
                    line=dict(color="#facc15", width=1.5, dash="dash")
                )
                fig.add_annotation(
                    x=x_label, y=1, xref="x", yref="paper",
                    text=str(x_label), showarrow=False,
                    font=dict(color="#facc15", size=11), yanchor="bottom"
                )

        fig.update_layout(
            **LAYOUT_DEFAULTS,
            height=320,
            showlegend=False,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#94a3b8"),
                       zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="#1e293b", tickformat=".2s",
                       tickprefix="Rp ", tickfont=dict(size=11, color="#94a3b8"),
                       zeroline=False),
            hovermode="x unified"
        )

    st.plotly_chart(fig, use_container_width=True)


# =====================================
# Profit vs Revenue Scatter
# =====================================

def profit_vs_revenue_chart(data):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No data available.")
        return

    fig = px.scatter(
        df,
        x="total_revenue",
        y="total_profit",
        size="total_units",
        hover_name="province",
        color_discrete_sequence=[CHART_COLORS[0]]
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=380
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================
# Daily Revenue Trend — drill down
# =====================================

def daily_trend_chart(data):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No daily data available.")
        return

    # Use full_date as x axis, format as "1 Apr", "2 Apr" etc
    if "full_date" in df.columns:
        df["full_date"] = pd.to_datetime(df["full_date"])
        df["label"] = df["full_date"].dt.strftime("%-d")
        # On Windows strftime doesn't support %-d, fallback:
        try:
            df["label"] = df["full_date"].dt.strftime("%-d")
        except Exception:
            df["label"] = df["day"].astype(str) if "day" in df.columns else df["full_date"].dt.strftime("%d")
    else:
        df["label"] = df["day"].astype(str)

    # Color weekends differently
    weekend_colors = []
    if "weekday" in df.columns:
        weekend_days = ["Sabtu", "Minggu", "Saturday", "Sunday"]
        weekend_colors = [
            "rgba(99,102,241,0.7)" if w in weekend_days else "rgba(59,130,246,0.85)"
            for w in df["weekday"]
        ]
    else:
        weekend_colors = ["rgba(59,130,246,0.85)"] * len(df)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["label"],
            y=df["total_revenue"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.12)",
            line=dict(color="#3b82f6", width=2.5),
            marker=dict(
                size=[
                    10 if (("weekday" in df.columns) and
                           (df.iloc[i]["weekday"] in ["Sabtu","Minggu","Saturday","Sunday"]))
                    else 5
                    for i in range(len(df))
                ],
                color=[
                    "#6366f1" if (("weekday" in df.columns) and
                                  (df.iloc[i]["weekday"] in ["Sabtu","Minggu","Saturday","Sunday"]))
                    else "#3b82f6"
                    for i in range(len(df))
                ],
                line=dict(color="#0f172a", width=1.5)
            ),
            hovertemplate=(
                "<b>Tgl %{x}</b>"
                + (" (%{customdata})" if "weekday" in df.columns else "")
                + "<br>Revenue: Rp %{y:,.0f}<extra></extra>"
            ),
            customdata=df["weekday"].tolist() if "weekday" in df.columns else None
        )
    )

    # Average line
    avg = df["total_revenue"].mean()
    fig.add_hline(
        y=avg,
        line_dash="dash",
        line_color="#facc15",
        line_width=1.5,
        annotation_text=f"Avg: Rp {avg:,.0f}",
        annotation_position="top right",
        annotation_font_color="#facc15",
        annotation_font_size=11
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=320,
        showlegend=False,
        bargap=0.15,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color="#94a3b8"),
            zeroline=False,
            title=dict(text="Tanggal", font=dict(color="#64748b", size=11))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1e293b",
            tickformat=".2s",
            tickprefix="Rp ",
            tickfont=dict(size=11, color="#94a3b8"),
            zeroline=False
        ),
        hovermode="x unified"
    )

    # Legend note
    st.markdown(
        "<p style='color:#64748b;font-size:0.75rem;margin:0 0 0.3rem 0;'>"
        "<span style='color:#6366f1;'>■</span> Weekend &nbsp;"
        "<span style='color:#3b82f6;'>■</span> Weekday &nbsp;"
        "<span style='color:#facc15;'>- -</span> Rata-rata</p>",
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True)