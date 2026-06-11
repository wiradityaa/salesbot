from .tools import (
    get_top_products, get_product_summary,
    get_province_revenue, get_province_comparison, get_top_products_in_province,
    get_category_revenue, get_category_by_province,
    get_monthly_trend, get_quarterly_trend, get_year_over_year,
    get_payment_revenue, get_payment_by_province,
    get_product_quadrants, get_province_recommendation,
    get_category_recommendation, get_general_summary
)

# -------------------------------------------------------
# Route intent → tool
# -------------------------------------------------------

def route(intent_data: dict) -> dict:
    """
    Terima intent dict dari classifier, panggil tool yang sesuai.
    Return hasil analytics/recommendation.
    """
    intent   = intent_data.get("intent", "general_summary")
    metric   = intent_data.get("metric")
    province = intent_data.get("province")
    category = intent_data.get("category")
    year     = intent_data.get("year")
    limit    = intent_data.get("limit") or 10

    # -------------------------------------------------------
    # Routing logic
    # -------------------------------------------------------

    if intent == "product_analysis":
        # Kalau ada province spesifik → top products di provinsi itu
        if province and not category:
            return get_top_products_in_province(province=province,
                                                 limit=limit, year=year)
        # Kalau ada category filter
        return get_top_products(metric=metric or "revenue",
                                province=province, category=category,
                                year=year, limit=limit)

    elif intent == "province_analysis":
        # Kalau province spesifik → top products di provinsi itu
        if province:
            return get_top_products_in_province(province=province,
                                                 limit=limit, year=year)
        # Kalau tidak → perbandingan semua provinsi
        return get_province_comparison(year=year)

    elif intent == "category_analysis":
        if province:
            return get_category_revenue(province=province, year=year)
        return get_category_revenue(year=year)

    elif intent == "trend_analysis":
        if metric == "quarter":
            return get_quarterly_trend(province=province, year=year)
        if year is None and province is None:
            return get_year_over_year()
        return get_monthly_trend(province=province, category=category, year=year)

    elif intent == "payment_analysis":
        if province:
            return get_payment_revenue(province=province, year=year)
        return get_payment_by_province(year=year)

    elif intent == "recommendation":
        if province:
            return get_product_quadrants(province=province, year=year)
        if category:
            return get_category_recommendation(province=province, year=year)
        # Default rekomendasi: quadrant analysis + province recommendation
        quadrant = get_product_quadrants(year=year)
        prov_rec = get_province_recommendation(year=year)
        return {
            "status": "success",
            "data": {
                "product_quadrants":       quadrant.get("data", []),
                "province_recommendation": prov_rec.get("data", [])
            }
        }

    elif intent == "general_summary":
        return get_general_summary(year=year)

    else:
        # out_of_scope
        return {"status": "out_of_scope", "data": [], "error": None}