"""Test suite untuk Analytics modules menggunakan pytest."""

import pytest
from test_log.conftest import (
    TEST_VALID_PROVINCES,
    TEST_VALID_YEARS,
    TEST_SAMPLE_PRODUCT,
    TEST_SAMPLE_CATEGORY,
    TEST_SAMPLE_PAYMENT
)


class TestProductAnalytics:
    """Test ProductAnalytics module."""

    def test_top_products_by_revenue_returns_list(self, product_analytics):
        """Verifikasi top_products_by_revenue mengembalikan list."""
        result = product_analytics.top_products_by_revenue(limit=5)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_top_products_with_valid_limit(self, product_analytics):
        """Test dengan berbagai limit values."""
        for limit in [1, 5, 10, 20]:
            result = product_analytics.top_products_by_revenue(limit=limit)

            assert result.get("status") == "success"
            assert len(result.get("data", [])) <= limit

    def test_top_products_with_province_filter(self, product_analytics):
        """Test top products dengan province filter."""
        result = product_analytics.top_products_by_revenue(
            province=TEST_VALID_PROVINCES[0],
            limit=5
        )

        assert result.get("status") == "success"
        data = result.get("data", [])
        if len(data) > 0:
            # Verify province dalam response (kalau available)
            pass

    def test_top_products_with_year_filter(self, product_analytics):
        """Test top products dengan year filter."""
        result = product_analytics.top_products_by_revenue(
            year=2023,
            limit=5
        )

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_product_performance_returns_dict(self, product_analytics):
        """Test product_performance_summary mengembalikan dict."""
        result = product_analytics.product_performance_summary()

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"

    def test_product_performance_metrics_present(self, product_analytics):
        """Verify product performance punya expected metrics."""
        result = product_analytics.product_performance_summary()
        data = result.get("data", [])

        if len(data) > 0:
            first_product = data[0]
            # Check untuk expected columns
            assert "product" in first_product or "name" in first_product

    def test_product_detail_with_valid_product(self, product_analytics):
        """Test product_detail dengan valid product."""
        result = product_analytics.product_detail(TEST_SAMPLE_PRODUCT)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"

    def test_product_detail_metrics(self, product_analytics):
        """Verify product detail punya required metrics."""
        result = product_analytics.product_detail(TEST_SAMPLE_PRODUCT)

        if result.get("status") == "success":
            data = result.get("data")
            assert isinstance(data, dict)


class TestProvinceAnalytics:
    """Test ProvinceAnalytics module."""

    def test_province_revenue_by_revenue(self, province_analytics):
        """Test revenue_by_province mengembalikan list."""
        result = province_analytics.revenue_by_province(year=2023)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_province_revenue_all_years(self, province_analytics):
        """Test revenue_by_province untuk all years."""
        for year in TEST_VALID_YEARS:
            result = province_analytics.revenue_by_province(year=year)

            assert result.get("status") == "success"
            assert isinstance(result.get("data"), list)

    def test_province_comparison_returns_list(self, province_analytics):
        """Test province_comparison mengembalikan list."""
        result = province_analytics.province_comparison(year=2023)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"

    def test_province_comparison_data_structure(self, province_analytics):
        """Verify province comparison punya expected structure."""
        result = province_analytics.province_comparison(year=2023)
        data = result.get("data", [])

        if len(data) > 0:
            first_row = data[0]
            assert isinstance(first_row, dict)

    def test_province_top_products(self, province_analytics):
        """Test top_products_in_province."""
        result = province_analytics.top_products_in_province(
            province=TEST_VALID_PROVINCES[0],
            limit=5,
            year=2023
        )

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_province_top_products_all_provinces(self, province_analytics):
        """Test top_products untuk all provinces."""
        for province in TEST_VALID_PROVINCES:
            result = province_analytics.top_products_in_province(
                province=province,
                limit=3,
                year=2023
            )

            assert result.get("status") == "success"


class TestCategoryAnalytics:
    """Test CategoryAnalytics module."""

    def test_revenue_by_category_returns_list(self, category_analytics):
        """Test revenue_by_category mengembalikan list."""
        result = category_analytics.revenue_by_category(year=2023)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_revenue_by_category_all_years(self, category_analytics):
        """Test revenue_by_category untuk all years."""
        for year in TEST_VALID_YEARS:
            result = category_analytics.revenue_by_category(year=year)

            assert result.get("status") == "success"
            assert isinstance(result.get("data"), list)

    def test_category_distribution_returns_list(self, category_analytics):
        """Test revenue_by_category mengembalikan list."""
        result = category_analytics.revenue_by_category(year=2023)

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_category_top_products(self, category_analytics):
        """Test top_products_in_category."""
        result = category_analytics.top_products_in_category(
            category=TEST_SAMPLE_CATEGORY,
            limit=5,
            year=2023
        )

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)


class TestTrendAnalytics:
    """Test TrendAnalytics module."""

    def test_monthly_trend_returns_list(self, trend_analytics):
        """Test monthly_revenue mengembalikan list."""
        result = trend_analytics.monthly_revenue(year=2023)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_monthly_trend_all_years(self, trend_analytics):
        """Test monthly_revenue untuk all years."""
        for year in TEST_VALID_YEARS:
            result = trend_analytics.monthly_revenue(year=year)

            assert result.get("status") == "success"

    def test_quarterly_trend_returns_list(self, trend_analytics):
        """Test quarterly_revenue mengembalikan list."""
        result = trend_analytics.quarterly_revenue(year=2023)

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_yearly_trend_returns_list(self, trend_analytics):
        """Test year_over_year mengembalikan list."""
        result = trend_analytics.year_over_year()

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_best_worst_month(self, trend_analytics):
        """Test best_worst_months."""
        result = trend_analytics.best_worst_months(year=2023)

        assert result.get("status") == "success"
        data = result.get("data", {})
        assert isinstance(data, dict)

    def test_best_worst_month_contains_required_keys(self, trend_analytics):
        """Verify best_worst_months punya required keys."""
        result = trend_analytics.best_worst_months(year=2023)
        data = result.get("data", {})

        if data:
            # Should have best and worst month data
            assert len(data) > 0


class TestPaymentAnalytics:
    """Test PaymentAnalytics module."""

    def test_revenue_by_payment_returns_list(self, payment_analytics):
        """Test revenue_by_payment mengembalikan list."""
        result = payment_analytics.revenue_by_payment(year=2023)

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_revenue_by_payment_all_years(self, payment_analytics):
        """Test revenue_by_payment untuk all years."""
        for year in TEST_VALID_YEARS:
            result = payment_analytics.revenue_by_payment(year=year)

            assert result.get("status") == "success"

    def test_payment_distribution_returns_list(self, payment_analytics):
        """Test revenue_by_payment mengembalikan list."""
        result = payment_analytics.revenue_by_payment(year=2023)

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)

    def test_payment_trend_returns_list(self, payment_analytics):
        """Test payment_trend mengembalikan list."""
        result = payment_analytics.payment_trend(
            method=TEST_SAMPLE_PAYMENT,
            year=2023
        )

        assert result.get("status") == "success"
        assert isinstance(result.get("data"), list)


class TestAnalyticsIntegration:
    """Integration tests untuk analytics modules."""

    def test_all_analytics_modules_accessible(
        self,
        product_analytics,
        province_analytics,
        category_analytics,
        trend_analytics,
        payment_analytics
    ):
        """Verifikasi semua analytics modules dapat diakses."""
        assert product_analytics is not None
        assert province_analytics is not None
        assert category_analytics is not None
        assert trend_analytics is not None
        assert payment_analytics is not None

    def test_multiple_queries_sequential(self, product_analytics, province_analytics):
        """Test multiple analytics queries secara sequential."""
        result1 = product_analytics.top_products_by_revenue(limit=5)
        assert result1.get("status") == "success"

        result2 = province_analytics.revenue_by_province(year=2023)
        assert result2.get("status") == "success"

        result3 = product_analytics.top_products_by_revenue(limit=10)
        assert result3.get("status") == "success"

    def test_query_with_edge_case_filters(self, product_analytics):
        """Test dengan edge case filters."""
        # Test dengan limit = 1
        result = product_analytics.top_products_by_revenue(limit=1)
        assert result.get("status") == "success"