from .db_utils import execute_query
from .product_analytics import _build_filters


class AlertAnalytics:
    """Deteksi anomali dan alert otomatis dari data penjualan."""

    THRESHOLD = 0.20  # 20% drop = alert

    # -------------------------------------------------------
    # Province revenue alerts
    # -------------------------------------------------------

    def province_alerts(self, year: int = None, province: str = None) -> list:
        """Bandingkan revenue provinsi bulan ini vs bulan lalu."""

        filters, params = _build_filters(province=province, year=year)

        sql = f"""
            WITH monthly AS (
                SELECT
                    l.province,
                    d.year,
                    d.month,
                    d.month_name,
                    SUM(f.revenue) AS revenue
                FROM fact_sales f
                JOIN dim_location l ON f.location_id = l.location_id
                JOIN dim_date     d ON f.date_id      = d.date_id
                {filters}
                GROUP BY l.province, d.year, d.month, d.month_name
            ),
            ranked AS (
                SELECT *,
                    LAG(revenue) OVER (
                        PARTITION BY province ORDER BY year, month
                    ) AS prev_revenue
                FROM monthly
            )
            SELECT * FROM ranked
            WHERE prev_revenue IS NOT NULL
            ORDER BY year DESC, month DESC
        """
        result = execute_query(sql, tuple(params))
        if result["status"] != "success":
            return []

        alerts = []
        seen = set()

        for row in result["data"]:
            prov = row["province"]
            if prov in seen:
                continue
            seen.add(prov)

            curr = float(row["revenue"] or 0)
            prev = float(row["prev_revenue"] or 0)

            if prev == 0:
                continue

            change_pct = (curr - prev) / prev

            if change_pct <= -self.THRESHOLD:
                alerts.append({
                    "type": "danger",
                    "icon": "⚠️",
                    "entity": "Province",
                    "name": prov,
                    "message": (
                        f"Revenue {prov} turun "
                        f"{abs(change_pct)*100:.1f}% "
                        f"(Rp {curr:,.0f} vs Rp {prev:,.0f})"
                    ),
                    "change_pct": change_pct
                })
            elif change_pct >= self.THRESHOLD:
                alerts.append({
                    "type": "success",
                    "icon": "📈",
                    "entity": "Province",
                    "name": prov,
                    "message": (
                        f"Revenue {prov} naik "
                        f"{change_pct*100:.1f}% "
                        f"(Rp {curr:,.0f} vs Rp {prev:,.0f})"
                    ),
                    "change_pct": change_pct
                })

        return alerts

    # -------------------------------------------------------
    # Product profit margin alerts
    # -------------------------------------------------------

    def product_alerts(self, year: int = None, limit: int = 5,
                       province: str = None) -> list:
        """Deteksi produk dengan profit margin turun signifikan."""

        filters, params = _build_filters(province=province, year=year)

        sql = f"""
            WITH monthly AS (
                SELECT
                    p.product_name,
                    d.year,
                    d.month,
                    ROUND(SUM(f.profit) / NULLIF(SUM(f.revenue),0) * 100, 2) AS margin
                FROM fact_sales f
                JOIN dim_product p ON f.product_id = p.product_id
                JOIN dim_location l ON f.location_id = l.location_id
                JOIN dim_date    d ON f.date_id      = d.date_id
                {filters}
                GROUP BY p.product_name, d.year, d.month
            ),
            ranked AS (
                SELECT *,
                    LAG(margin) OVER (
                        PARTITION BY product_name ORDER BY year, month
                    ) AS prev_margin
                FROM monthly
            )
            SELECT * FROM ranked
            WHERE prev_margin IS NOT NULL
            ORDER BY year DESC, month DESC
        """
        result = execute_query(sql, tuple(params))
        if result["status"] != "success":
            return []

        alerts = []
        seen = set()

        for row in result["data"]:
            name = row["product_name"]
            if name in seen:
                continue
            seen.add(name)

            curr = float(row["margin"] or 0)
            prev = float(row["prev_margin"] or 0)

            if prev == 0:
                continue

            drop = prev - curr
            if drop >= 5:  # 5 percentage points drop
                alerts.append({
                    "type": "warning",
                    "icon": "📉",
                    "entity": "Product",
                    "name": name,
                    "message": (
                        f"Margin {name} turun "
                        f"{drop:.1f}pp "
                        f"({curr:.1f}% vs {prev:.1f}%)"
                    ),
                    "change_pct": -drop / 100
                })

            if len(alerts) >= limit:
                break

        return alerts

    # -------------------------------------------------------
    # Payment method alerts
    # -------------------------------------------------------

    def payment_alerts(self, year: int = None, province: str = None) -> list:
        """Deteksi perubahan signifikan metode pembayaran."""

        filters, params = _build_filters(province=province, year=year)

        sql = f"""
            WITH monthly AS (
                SELECT
                    pm.payment_method,
                    d.year,
                    d.month,
                    COUNT(*) AS txn_count
                FROM fact_sales f
                JOIN dim_payment pm ON f.payment_id  = pm.payment_id
                JOIN dim_location l ON f.location_id = l.location_id
                JOIN dim_date    d  ON f.date_id      = d.date_id
                {filters}
                GROUP BY pm.payment_method, d.year, d.month
            ),
            ranked AS (
                SELECT *,
                    LAG(txn_count) OVER (
                        PARTITION BY payment_method ORDER BY year, month
                    ) AS prev_count
                FROM monthly
            )
            SELECT * FROM ranked
            WHERE prev_count IS NOT NULL
            ORDER BY year DESC, month DESC
        """
        result = execute_query(sql, tuple(params))
        if result["status"] != "success":
            return []

        alerts = []
        seen = set()

        for row in result["data"]:
            method = row["payment_method"]
            if method in seen:
                continue
            seen.add(method)

            curr = float(row["txn_count"] or 0)
            prev = float(row["prev_count"] or 0)

            if prev == 0:
                continue

            change_pct = (curr - prev) / prev

            if change_pct <= -self.THRESHOLD:
                alerts.append({
                    "type": "warning",
                    "icon": "💳",
                    "entity": "Payment",
                    "name": method,
                    "message": (
                        f"Transaksi {method} turun "
                        f"{abs(change_pct)*100:.1f}% "
                        f"({int(curr):,} vs {int(prev):,} transaksi)"
                    ),
                    "change_pct": change_pct
                })
            elif change_pct >= self.THRESHOLD:
                alerts.append({
                    "type": "success",
                    "icon": "💳",
                    "entity": "Payment",
                    "name": method,
                    "message": (
                        f"Transaksi {method} naik "
                        f"{change_pct*100:.1f}% "
                        f"({int(curr):,} vs {int(prev):,} transaksi)"
                    ),
                    "change_pct": change_pct
                })

        return alerts

    # -------------------------------------------------------
    # All alerts combined
    # -------------------------------------------------------

    def get_all_alerts(self, year: int = None, province: str = None) -> list:
        """Gabungkan semua alert, urutkan dari yang paling kritis."""
        alerts = (
            self.province_alerts(year=year, province=province) +
            self.product_alerts(year=year, province=province) +
            self.payment_alerts(year=year, province=province)
        )
        # Sort: danger first, then warning, then success
        order = {"danger": 0, "warning": 1, "success": 2}
        alerts.sort(key=lambda x: (order.get(x["type"], 3), x["change_pct"]))
        return alerts