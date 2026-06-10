from .db_utils import execute_query
from .product_analytics import _build_filters

class PaymentAnalytics:
    """Analitik berbasis metode pembayaran."""

    # -------------------------------------------------------
    # Revenue by payment method
    # -------------------------------------------------------

    def revenue_by_payment(self, province: str = None,
                            year: int = None) -> dict:
        """Revenue dan transaksi per metode pembayaran."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                pm.payment_method,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS transaction_share_pct
            FROM fact_sales f
            JOIN dim_payment  pm ON f.payment_id  = pm.payment_id
            JOIN dim_location l  ON f.location_id = l.location_id
            JOIN dim_date     d  ON f.date_id      = d.date_id
            {filters}
            GROUP BY pm.payment_method
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Payment method per province
    # -------------------------------------------------------

    def payment_by_province(self, year: int = None) -> dict:
        """Distribusi metode pembayaran per provinsi."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                l.province,
                pm.payment_method,
                COUNT(*)       AS transaction_count,
                SUM(f.revenue) AS total_revenue
            FROM fact_sales f
            JOIN dim_payment  pm ON f.payment_id  = pm.payment_id
            JOIN dim_location l  ON f.location_id = l.location_id
            JOIN dim_date     d  ON f.date_id      = d.date_id
            {filters}
            GROUP BY l.province, pm.payment_method
            ORDER BY l.province, transaction_count DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Payment trend over time
    # -------------------------------------------------------

    def payment_trend(self, year: int = None) -> dict:
        """Tren penggunaan metode pembayaran per bulan."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                d.year,
                d.month,
                d.month_name,
                pm.payment_method,
                COUNT(*)       AS transaction_count,
                SUM(f.revenue) AS total_revenue
            FROM fact_sales f
            JOIN dim_payment pm ON f.payment_id = pm.payment_id
            JOIN dim_date    d  ON f.date_id     = d.date_id
            {filters}
            GROUP BY d.year, d.month, d.month_name, pm.payment_method
            ORDER BY d.year, d.month, pm.payment_method
        """
        return execute_query(sql, tuple(params))