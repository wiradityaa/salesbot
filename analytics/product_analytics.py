from .db_utils import execute_query

class ProductAnalytics:
    """Analitik berbasis produk."""

    # -------------------------------------------------------
    # Top products by revenue
    # -------------------------------------------------------

    def top_products_by_revenue(self, limit: int = 10, province: str = None,
                                 category: str = None, year: int = None) -> dict:
        """Top N produk berdasarkan total revenue."""
        filters, params = _build_filters(province=province, category=category, year=year)
        sql = f"""
            SELECT
                p.product_name,
                p.category,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.units_sold) AS total_units,
                SUM(f.profit)     AS total_profit,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct
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
    # Top products by units sold
    # -------------------------------------------------------

    def top_products_by_units(self, limit: int = 10, province: str = None,
                               year: int = None) -> dict:
        """Top N produk berdasarkan total units terjual."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                p.product_name,
                p.category,
                SUM(f.units_sold) AS total_units,
                SUM(f.revenue)    AS total_revenue
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY p.product_name, p.category
            ORDER BY total_units DESC
            LIMIT %s
        """
        params.append(limit)
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Product performance summary (untuk quadrant analysis)
    # -------------------------------------------------------

    def product_performance_summary(self, province: str = None,
                                     year: int = None) -> dict:
        """Semua produk dengan revenue, volume, profit — untuk quadrant classifier."""
        filters, params = _build_filters(province=province, year=year)
        sql = f"""
            SELECT
                p.product_name,
                p.category,
                SUM(f.units_sold) AS total_units,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue), 0) * 100, 2) AS profit_margin_pct,
                COUNT(*)          AS transaction_count
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {filters}
            GROUP BY p.product_name, p.category
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params))

    # -------------------------------------------------------
    # Single product detail
    # -------------------------------------------------------

    def product_detail(self, product_name: str, year: int = None) -> dict:
        """Detail performa satu produk spesifik."""
        filters, params = _build_filters(year=year)
        params_with_product = [product_name] + params
        where = f"WHERE p.product_name = %s" + (filters.replace("WHERE", "AND") if filters else "")
        sql = f"""
            SELECT
                p.product_name,
                p.category,
                l.province,
                SUM(f.units_sold) AS total_units,
                SUM(f.revenue)    AS total_revenue,
                SUM(f.profit)     AS total_profit,
                ROUND(AVG(f.unit_price), 2) AS avg_price
            FROM fact_sales f
            JOIN dim_product  p ON f.product_id  = p.product_id
            JOIN dim_location l ON f.location_id = l.location_id
            JOIN dim_date     d ON f.date_id      = d.date_id
            {where}
            GROUP BY p.product_name, p.category, l.province
            ORDER BY total_revenue DESC
        """
        return execute_query(sql, tuple(params_with_product))


# -------------------------------------------------------
# Filter builder (shared helper)
# -------------------------------------------------------

def _build_filters(province: str = None, category: str = None,
                   year: int = None) -> tuple:
    """Bangun WHERE clause dan params list dari filter opsional."""
    clauses = []
    params  = []

    if province:
        clauses.append("l.province = %s")
        params.append(province)
    if category:
        clauses.append("p.category = %s")
        params.append(category)
    if year:
        clauses.append("d.year = %s")
        params.append(year)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where, params