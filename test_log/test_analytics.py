# test_analytics.py (taruh di root folder, jalankan sekali, hapus setelah selesai)

from analytics import (
    ProductAnalytics, ProvinceAnalytics,
    CategoryAnalytics, TrendAnalytics, PaymentAnalytics
)

product  = ProductAnalytics()
province = ProvinceAnalytics()
category = CategoryAnalytics()
trend    = TrendAnalytics()
payment  = PaymentAnalytics()

tests = [
    ("top_products_by_revenue",      product.top_products_by_revenue(limit=5)),
    ("top_products_by_units",        product.top_products_by_units(limit=5)),
    ("product_performance_summary",  product.product_performance_summary()),
    ("revenue_by_province",          province.revenue_by_province()),
    ("top_products_in_province",     province.top_products_in_province("Jawa Barat")),
    ("revenue_by_category",          category.revenue_by_category()),
    ("category_by_province",         category.category_by_province()),
    ("monthly_revenue",              trend.monthly_revenue()),
    ("quarterly_revenue",            trend.quarterly_revenue()),
    ("year_over_year",               trend.year_over_year()),
    ("revenue_by_payment",           payment.revenue_by_payment()),
    ("payment_by_province",          payment.payment_by_province()),
]

print("=" * 55)
print("Analytics Engine: Testing SQL Query Execution")
print("=" * 55)

passed = 0
for name, result in tests:
    status = result["status"]
    rows   = result["row_count"]
    error  = result["error"]
    if status == "success" and rows > 0:
        print(f"  [PASS] {name:<35} {rows} rows")
        passed += 1
    else:
        print(f"  [FAIL] {name:<35} {error}")

print("=" * 55)
print(f"Result: {passed}/{len(tests)} passed")
print("=" * 55)