from .db_utils import execute_query
from .product_analytics import _build_filters

class TrendAnalytics:
    """Analitik tren waktu."""

    # -------------------------------------------------------
    # Monthly revenue trend
    # -------------------------------------------------------

    def monthly_revenue(self, province: str = None,
                         category: str = None, year: int = None) -> dict:
        """Tren revenue per bulan."""
        filters, params = _build_filters(province=province, category=category, year=year)
        sql = f"""
            SELECT
                d.year,
                d.month,
                d.month_name,
                d.quarter,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY d.year, d.month, d.month_name, d.quarter
            ORDER BY d.year, d.month
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Quarterly revenue
    # -------------------------------------------------------

    def quarterly_revenue(self, province: str = None,
                           year: int = None) -> dict:
        """Revenue per kuartal."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                d.year,
                d.quarter,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY d.year, d.quarter
            ORDER BY d.year, d.quarter
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Year over year comparison
    # -------------------------------------------------------

    def year_over_year(self, province: str = None) -> dict:
        """Perbandingan revenue antar tahun."""
        filters, params = _build_filters(province=province)
        sql = f"""
            SELECT
                d.year,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count
            FROM fact_sales f
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY d.year
            ORDER BY d.year
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Best and worst month
    # -------------------------------------------------------

    def best_worst_months(self, year: int = None) -> dict:
        """Bulan dengan revenue tertinggi dan terendah."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                d.year,
                d.month,
                d.month_name,
                SUM(f.revenue) AS total_revenue
            FROM fact_sales f
            JOIN dim_date d ON f.date_id = d.date_id
            {filters}
            GROUP BY d.year, d.month, d.month_name
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))