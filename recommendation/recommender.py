from analytics import ProductAnalytics, ProvinceAnalytics

product_analytics  = ProductAnalytics()
province_analytics = ProvinceAnalytics()

# -------------------------------------------------------
# Product Quadrant Classifier
# -------------------------------------------------------

def classify_product_quadrants(province: str = None, year: int = None) -> dict:
    """
    Klasifikasi produk ke 4 kuadran berdasarkan volume dan profit.
    Q1 Stars        : volume tinggi, profit tinggi
    Q2 Cash Cows    : volume rendah, profit tinggi
    Q3 Question Marks: volume tinggi, profit rendah
    Q4 Dogs         : volume rendah, profit rendah
    """
    result = product_analytics.product_performance_summary(province=province, year=year)

    if result["status"] != "success" or not result["data"]:
        return {"status": "error", "data": [], "error": result.get("error", "No data")}

    data = result["data"]

    # Hitung median sebagai threshold
    volumes = sorted([r["total_units"] for r in data])
    profits = sorted([r["total_profit"] for r in data])

    median_volume = _median(volumes)
    median_profit = _median(profits)

    classified = []
    for row in data:
        vol  = row["total_units"]
        prof = row["total_profit"]

        if vol >= median_volume and prof >= median_profit:
            quadrant = "Stars"
            description = "Volume tinggi & profit tinggi — pertahankan dan kembangkan"
        elif vol < median_volume and prof >= median_profit:
            quadrant = "Cash Cows"
            description = "Volume rendah tapi profit tinggi — jaga stabilitas harga"
        elif vol >= median_volume and prof < median_profit:
            quadrant = "Question Marks"
            description = "Volume tinggi tapi profit rendah — evaluasi struktur biaya"
        else:
            quadrant = "Dogs"
            description = "Volume rendah & profit rendah — pertimbangkan untuk dikurangi"

        classified.append({
            **row,
            "quadrant": quadrant,
            "quadrant_description": description
        })

    # Urutkan: Stars dulu, lalu Cash Cows, Question Marks, Dogs
    order = {"Stars": 0, "Cash Cows": 1, "Question Marks": 2, "Dogs": 3}
    classified.sort(key=lambda x: (order[x["quadrant"]], -x["total_revenue"]))

    return {
        "status": "success",
        "data": classified,
        "metadata": {
            "median_volume": median_volume,
            "median_profit": median_profit,
            "province_filter": province,
            "year_filter": year
        }
    }


# -------------------------------------------------------
# Province Recommender
# -------------------------------------------------------

def recommend_by_province(year: int = None) -> dict:
    """
    Rekomendasi per provinsi berdasarkan performa vs rata-rata nasional.
    """
    result = province_analytics.revenue_by_province(year=year)

    if result["status"] != "success" or not result["data"]:
        return {"status": "error", "data": [], "error": result.get("error", "No data")}

    data = result["data"]

    # Hitung rata-rata nasional
    total_revenues = [r["total_revenue"] for r in data]
    total_profits  = [r["total_profit"]  for r in data]
    avg_revenue    = sum(total_revenues) / len(total_revenues)
    avg_profit     = sum(total_profits)  / len(total_profits)

    recommended = []
    for row in data:
        rev  = row["total_revenue"]
        prof = row["total_profit"]
        margin = row["profit_margin_pct"]

        # Tentukan status vs rata-rata nasional
        rev_vs_avg  = ((rev  - avg_revenue) / avg_revenue * 100) if avg_revenue else 0
        prof_vs_avg = ((prof - avg_profit)  / avg_profit  * 100) if avg_profit  else 0

        # Generate rekomendasi berdasarkan rule
        if rev > avg_revenue and margin >= 20:
            status = "High Performer"
            recommendation = (
                f"{row['province']} berada di atas rata-rata nasional dalam revenue "
                f"dan margin. Pertahankan strategi saat ini dan eksplorasi produk baru."
            )
        elif rev > avg_revenue and margin < 20:
            status = "High Revenue, Low Margin"
            recommendation = (
                f"{row['province']} memiliki revenue tinggi tapi margin rendah. "
                f"Evaluasi struktur biaya operasional dan harga jual."
            )
        elif rev < avg_revenue and margin >= 20:
            status = "Low Revenue, High Margin"
            recommendation = (
                f"{row['province']} memiliki margin bagus tapi volume rendah. "
                f"Tingkatkan penetrasi pasar dan frekuensi promosi."
            )
        else:
            status = "Needs Attention"
            recommendation = (
                f"{row['province']} berada di bawah rata-rata nasional. "
                f"Lakukan analisis mendalam terhadap produk dan saluran distribusi."
            )

        recommended.append({
            **row,
            "status": status,
            "recommendation": recommendation,
            "revenue_vs_national_avg_pct": round(rev_vs_avg, 2),
            "profit_vs_national_avg_pct":  round(prof_vs_avg, 2)
        })

    recommended.sort(key=lambda x: -x["total_revenue"])

    return {
        "status": "success",
        "data": recommended,
        "metadata": {
            "national_avg_revenue": round(avg_revenue, 2),
            "national_avg_profit":  round(avg_profit, 2),
            "year_filter": year
        }
    }


# -------------------------------------------------------
# Category Recommender
# -------------------------------------------------------

def recommend_by_category(province: str = None, year: int = None) -> dict:
    """
    Rekomendasi fokus kategori berdasarkan profit margin dan volume.
    """
    from analytics import CategoryAnalytics
    category_analytics = CategoryAnalytics()
    result = category_analytics.revenue_by_category(province=province, year=year)

    if result["status"] != "success" or not result["data"]:
        return {"status": "error", "data": [], "error": result.get("error", "No data")}

    data   = result["data"]
    margins = [r["profit_margin_pct"] for r in data]
    avg_margin = sum(margins) / len(margins) if margins else 0

    recommended = []
    for row in data:
        margin = row["profit_margin_pct"]

        if margin >= avg_margin * 1.1:
            action = "Prioritaskan — margin di atas rata-rata, tingkatkan stok dan promosi"
        elif margin >= avg_margin * 0.9:
            action = "Pertahankan — margin stabil, monitor tren harga bahan baku"
        else:
            action = "Evaluasi — margin di bawah rata-rata, tinjau efisiensi operasional"

        recommended.append({
            **row,
            "action": action,
            "vs_avg_margin_pct": round(margin - avg_margin, 2)
        })

    return {
        "status": "success",
        "data": recommended,
        "metadata": {
            "avg_margin_pct": round(avg_margin, 2),
            "province_filter": province,
            "year_filter": year
        }
    }


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def _median(sorted_list: list) -> float:
    """Hitung median dari list yang sudah diurutkan."""
    n = len(sorted_list)
    if n == 0:
        return 0
    mid = n // 2
    return (sorted_list[mid] + sorted_list[~mid]) / 2