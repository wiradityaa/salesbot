import streamlit as st


def kpi_card(title: str, value, icon: str = "📊", delta: float = None):
    """
    KPI card matching the dashboard screenshot.

    Parameters
    ----------
    title   : str   — label shown above the value
    value   : any   — formatted string or number to display
    icon    : str   — emoji icon
    delta   : float — optional percentage change vs previous period
                      positive = green ▲, negative = red ▼, None = hide
    """

    # Build delta HTML
    if delta is not None:
        if delta >= 0:
            delta_html = (
                f'<p style="color:#22c55e;font-size:0.78rem;margin:4px 0 0 0;">'
                f'▲ {abs(delta):.1f}% vs previous period</p>'
            )
        else:
            delta_html = (
                f'<p style="color:#ef4444;font-size:0.78rem;margin:4px 0 0 0;">'
                f'▼ {abs(delta):.1f}% vs previous period</p>'
            )
    else:
        delta_html = ""

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            padding: 1.2rem 1.4rem;
            border-radius: 14px;
            border: 1px solid #334155;
            min-height: 120px;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="
                font-size: 1.8rem;
                background: #1e3a5f;
                border-radius: 10px;
                width: 52px;
                height: 52px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            ">
                {icon}
            </div>

            <div>
                <p style="
                    color: #94a3b8;
                    font-size: 0.78rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0;
                ">
                    {title}
                </p>

                <p style="
                    color: #f1f5f9;
                    font-size: 1.6rem;
                    font-weight: 700;
                    margin: 4px 0 0 0;
                    line-height: 1.2;
                ">
                    {value}
                </p>

                {delta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )