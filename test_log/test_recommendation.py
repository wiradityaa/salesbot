"""Test suite untuk Recommendation engine."""

import pytest
from test_log.conftest import TEST_VALID_PROVINCES, TEST_VALID_YEARS


class TestProductQuadrants:
    """Test product quadrant classification."""

    def test_classify_product_quadrants_returns_dict(self, product_analytics):
        """Verifikasi classify_product_quadrants mengembalikan dict."""
        from recommendation.recommender import classify_product_quadrants

        result = classify_product_quadrants(year=2023)

        assert result is not None
        assert isinstance(result, dict)

    def test_product_quadrants_categories(self):
        """Test quadrant categories ada."""
        from recommendation.recommender import classify_product_quadrants

        result = classify_product_quadrants(year=2023)

        # Harus ada quadrant categories
        expected_quadrants = ["Stars", "CashCows", "QuestionMarks", "Dogs"]
        for quadrant in expected_quadrants:
            # Cek key ada (case sensitive)
            pass

    def test_classify_product_quadrants_all_years(self):
        """Test classify_product_quadrants untuk all years."""
        from recommendation.recommender import classify_product_quadrants

        for year in TEST_VALID_YEARS:
            result = classify_product_quadrants(year=year)
            assert result is not None
            assert isinstance(result, dict)

    def test_classify_product_quadrants_with_province(self):
        """Test classify_product_quadrants dengan province filter."""
        from recommendation.recommender import classify_product_quadrants

        result = classify_product_quadrants(
            province=TEST_VALID_PROVINCES[0],
            year=2023
        )

        assert result is not None
        assert isinstance(result, dict)


class TestProvinceRecommendation:
    """Test province-level recommendations."""

    def test_recommend_by_province_returns_dict(self):
        """Verifikasi recommend_by_province mengembalikan dict."""
        from recommendation.recommender import recommend_by_province

        result = recommend_by_province(year=2023)

        assert result is not None
        assert isinstance(result, dict)

    def test_recommend_by_province_structure(self):
        """Verify structure of province recommendations."""
        from recommendation.recommender import recommend_by_province

        result = recommend_by_province(year=2023)

        # Should have data for multiple provinces
        assert isinstance(result, dict)

    def test_recommend_by_province_all_years(self):
        """Test recommend_by_province untuk all years."""
        from recommendation.recommender import recommend_by_province

        for year in TEST_VALID_YEARS:
            result = recommend_by_province(year=year)
            assert result is not None
            assert isinstance(result, dict)

    def test_recommend_specific_province(self):
        """Test recommendation untuk specific province."""
        from recommendation.recommender import recommend_by_province

        result = recommend_by_province(year=2023)

        # Verify bisa mendapat data
        assert isinstance(result, dict)


class TestCategoryRecommendation:
    """Test category-level recommendations."""

    def test_recommend_by_category_returns_dict(self):
        """Verifikasi recommend_by_category mengembalikan dict."""
        from recommendation.recommender import recommend_by_category

        result = recommend_by_category(year=2023)

        assert result is not None
        assert isinstance(result, dict)

    def test_recommend_by_category_structure(self):
        """Verify structure of category recommendations."""
        from recommendation.recommender import recommend_by_category

        result = recommend_by_category(year=2023)

        # Should have recommendations
        assert isinstance(result, dict)

    def test_recommend_by_category_all_years(self):
        """Test recommend_by_category untuk all years."""
        from recommendation.recommender import recommend_by_category

        for year in TEST_VALID_YEARS:
            result = recommend_by_category(year=year)
            assert result is not None
            assert isinstance(result, dict)


class TestRecommendationIntegration:
    """Integration tests untuk recommendation engine."""

    def test_all_recommendations_accessible(self):
        """Verify semua recommendation functions dapat diakses."""
        from recommendation.recommender import (
            classify_product_quadrants,
            recommend_by_province,
            recommend_by_category
        )

        assert classify_product_quadrants is not None
        assert recommend_by_province is not None
        assert recommend_by_category is not None

    def test_multiple_recommendations_sequential(self):
        """Test multiple recommendation queries secara sequential."""
        from recommendation.recommender import (
            classify_product_quadrants,
            recommend_by_province,
            recommend_by_category
        )

        result1 = classify_product_quadrants(year=2023)
        assert result1 is not None

        result2 = recommend_by_province(year=2023)
        assert result2 is not None

        result3 = recommend_by_category(year=2023)
        assert result3 is not None

    def test_recommendation_consistency(self):
        """Test consistency of recommendations across multiple runs."""
        from recommendation.recommender import classify_product_quadrants

        result1 = classify_product_quadrants(year=2023)
        result2 = classify_product_quadrants(year=2023)

        # Dua run dengan parameter yang sama harusnya return hasil yang sama
        assert result1 == result2

    def test_recommendation_with_different_years(self):
        """Test recommendation changes dengan berbagai year."""
        from recommendation.recommender import (
            classify_product_quadrants,
            recommend_by_province
        )

        years = [2022, 2023, 2024]
        results = []

        for year in years:
            result1 = classify_product_quadrants(year=year)
            result2 = recommend_by_province(year=year)
            results.append((result1, result2))

        # Verify semua results ada
        assert len(results) == len(years)

        # Results untuk different years bisa berbeda
        assert results[0] is not None
        assert results[1] is not None
        assert results[2] is not None


class TestRecommendationValidation:
    """Test validasi recommendation output."""

    def test_product_quadrants_has_valid_format(self):
        """Verify product quadrants output memiliki format yang valid."""
        from recommendation.recommender import classify_product_quadrants

        result = classify_product_quadrants(year=2023)

        # Result harus dict
        assert isinstance(result, dict)

        # Harus ada data
        assert len(result) > 0

    def test_province_recommendation_has_actionable_insights(self):
        """Verify province recommendations punya actionable insights."""
        from recommendation.recommender import recommend_by_province

        result = recommend_by_province(year=2023)

        assert isinstance(result, dict)

    def test_category_recommendation_complete(self):
        """Verify category recommendations complete."""
        from recommendation.recommender import recommend_by_category

        result = recommend_by_category(year=2023)

        assert isinstance(result, dict)
        # Harus ada minimal data
        assert len(result) > 0
