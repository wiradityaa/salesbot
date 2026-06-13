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

def monthly_trend_chart(data, highlight_month: int = None):

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No trend data available.")
        return

    # Support both month_name and month columns
    x_col = "month_name" if "month_name" in df.columns else "month"

    # Marker sizes — highlight selected month
    if highlight_month is not None and "month" in df.columns:
        marker_sizes = [
            14 if int(row["month"]) == highlight_month else 6
            for _, row in df.iterrows()
        ]
        marker_colors = [
            "#facc15" if int(row["month"]) == highlight_month else "#3b82f6"
            for _, row in df.iterrows()
        ]
    else:
        marker_sizes  = [6] * len(df)
        marker_colors = ["#3b82f6"] * len(df)

    fig = go.Figure()

    # Filled area
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df["total_revenue"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.15)",
            line=dict(color="#3b82f6", width=2.5),
            marker=dict(
                size=marker_sizes,
                color=marker_colors,
                line=dict(color="#0f172a", width=1.5)
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: Rp %{y:,.0f}<extra></extra>"
            )
        )
    )

    # Vertical line for highlighted month
    # add_vline doesn't support categorical x-axis, use add_shape instead
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
                x=x_label,
                y=1,
                xref="x",
                yref="paper",
                text=str(x_label),
                showarrow=False,
                font=dict(color="#facc15", size=11),
                yanchor="bottom"
            )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        height=320,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#94a3b8"),
            zeroline=False
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