from analytics import (
    ProductAnalytics, ProvinceAnalytics,
    CategoryAnalytics, TrendAnalytics, PaymentAnalytics
)
from recommendation import (
    classify_product_quadrants,
    recommend_by_province,
    recommend_by_category
)

# Inisialisasi analytics classes
_product  = ProductAnalytics()
_province = ProvinceAnalytics()
_category = CategoryAnalytics()
_trend    = TrendAnalytics()
_payment  = PaymentAnalytics()

# -------------------------------------------------------
# Tool functions — dipanggil oleh tool_router
# -------------------------------------------------------

def get_top_products(metric: str = "revenue", province: str = None,
                     category: str = None, year: int = None,
                     limit: int = 10) -> dict:
    limit = limit or 10
    if metric == "units":
        return _product.top_products_by_units(limit=limit, province=province, year=year)
    return _product.top_products_by_revenue(limit=limit, province=province,
                                             category=category, year=year)

def get_product_summary(province: str = None, year: int = None) -> dict:
    return _product.product_performance_summary(province=province, year=year)

def get_province_revenue(year: int = None) -> dict:
    return _province.revenue_by_province(year=year)

def get_province_comparison(year: int = None) -> dict:
    return _province.province_comparison(year=year)

def get_top_products_in_province(province: str, limit: int = 5,
                                  year: int = None) -> dict:
    return _province.top_products_in_province(province=province,
                                               limit=limit, year=year)

def get_category_revenue(province: str = None, year: int = None) -> dict:
    return _category.revenue_by_category(province=province, year=year)

def get_category_by_province(year: int = None) -> dict:
    return _category.category_by_province(year=year)

def get_monthly_trend(province: str = None, category: str = None,
                      year: int = None) -> dict:
    return _trend.monthly_revenue(province=province, category=category, year=year)

def get_quarterly_trend(province: str = None, year: int = None) -> dict:
    return _trend.quarterly_revenue(province=province, year=year)

def get_year_over_year(province: str = None) -> dict:
    return _trend.year_over_year(province=province)

def get_payment_revenue(province: str = None, year: int = None) -> dict:
    return _payment.revenue_by_payment(province=province, year=year)

def get_payment_by_province(year: int = None) -> dict:
    return _payment.payment_by_province(year=year)

def get_product_quadrants(province: str = None, year: int = None) -> dict:
    return classify_product_quadrants(province=province, year=year)

def get_province_recommendation(year: int = None) -> dict:
    return recommend_by_province(year=year)

def get_category_recommendation(province: str = None, year: int = None) -> dict:
    return recommend_by_category(province=province, year=year)

def get_general_summary(year: int = None) -> dict:
    """Gabungkan data utama untuk ringkasan bisnis."""
    revenue  = _province.revenue_by_province(year=year)
    category = _category.revenue_by_category(year=year)
    trend    = _trend.monthly_revenue(year=year)
    return {
        "status": "success",
        "data": {
            "province_summary": revenue.get("data", []),
            "category_summary": category.get("data", []),
            "monthly_trend":    trend.get("data", [])
        }
    }