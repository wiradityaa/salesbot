from .db_utils import execute_query
from .product_analytics import _build_filters

class CategoryAnalytics:
    """Analitik berbasis kategori produk."""

    # -------------------------------------------------------
    # Revenue per category
    # -------------------------------------------------------

    def revenue_by_category(self, province: str = None,
                             year: int = None) -> dict:
        """Total revenue dan profit per kategori."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                p.category,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                SUM(f.units_sold) AS total_units,
                COUNT(*)          AS transaction_count,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct,
                COUNT(DISTINCT p.product_name) AS product_count
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Category breakdown per province
    # -------------------------------------------------------

    def category_by_province(self, year: int = None) -> dict:
        """Distribusi kategori di setiap provinsi."""
        filters, params = _build_filters(year=year)
        sql = f"""
            SELECT
                l.province,
                p.category,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.units_sold) AS total_units
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY l.province, p.category
            ORDER BY l.province, total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Top products in category
    # -------------------------------------------------------

    def top_products_in_category(self, category: str,
                                  limit: int = 5, year: int = None) -> dict:
        """Top produk dalam satu kategori."""
        filters, params = _build_filters(category=category, year=year)
        sql = f"""
            SELECT
                p.product_name,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.units_sold) AS total_units,
                SUM(f.profit)     AS total_profit,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY p.product_name
            ORDER BY total_revenue DESC
            LIMIT %s
        """
        params.append(limit)
        return execute_query(sql, tuple(params))