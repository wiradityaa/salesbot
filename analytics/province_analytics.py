from .db_utils import execute_query
from .product_analytics import _build_filters

class ProvinceAnalytics:
    """Analitik berbasis provinsi."""

    # -------------------------------------------------------
    # Revenue per province
    # -------------------------------------------------------

    def revenue_by_province(self, year: int = None) -> dict:
        """Total revenue, profit, transaksi per provinsi."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                l.province,
                SUM(f.revenue)                AS total_revenue,
                SUM(f.profit)                 AS total_profit,
                SUM(f.units_sold)             AS total_units,
                COUNT(*)                      AS transaction_count,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY l.province
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Top products per province
    # -------------------------------------------------------

    def top_products_in_province(self, province: str,
                                  limit: int = 5, year: int = None) -> dict:
        """Top produk di satu provinsi tertentu."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                p.product_name,
                p.category,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.units_sold) AS total_units,
                SUM(f.profit)     AS total_profit
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY p.product_name, p.category
            ORDER BY total_revenue DESC
            LIMIT %s
        """
        params.append(limit)
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Province comparison
    # -------------------------------------------------------

    def province_comparison(self, year: int = None) -> dict:
        """Perbandingan antar provinsi dengan metrik lengkap."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                l.province,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count,
                ROUND(AVG(f.revenue), 2) AS avg_transaction_value,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY l.province
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Monthly trend per province
    # -------------------------------------------------------

    def monthly_trend_by_province(self, province: str, year: int = None) -> dict:
        """Tren bulanan revenue untuk satu provinsi."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                d.year,
                d.month,
                d.month_name,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.units_sold) AS total_units
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY d.year, d.month, d.month_name
            ORDER BY d.year, d.month
        """
        return execute_query(sql, tuple(params))