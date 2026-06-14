"""Pytest fixtures dan setup untuk testing SalesBot modules."""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from analytics.product_analytics import ProductAnalytics
from analytics.province_analytics import ProvinceAnalytics
from analytics.category_analytics import CategoryAnalytics
from analytics.trend_analytics import TrendAnalytics
from analytics.payment_analytics import PaymentAnalytics
from recommendation.recommender import (
    classify_product_quadrants,
    recommend_by_province,
    recommend_by_category
)


@pytest.fixture(scope="session")
def product_analytics():
    """Initialize ProductAnalytics instance."""
    return ProductAnalytics()


@pytest.fixture(scope="session")
def province_analytics():
    """Initialize ProvinceAnalytics instance."""
    return ProvinceAnalytics()


@pytest.fixture(scope="session")
def category_analytics():
    """Initialize CategoryAnalytics instance."""
    return CategoryAnalytics()


@pytest.fixture(scope="session")
def trend_analytics():
    """Initialize TrendAnalytics instance."""
    return TrendAnalytics()


@pytest.fixture(scope="session")
def payment_analytics():
    """Initialize PaymentAnalytics instance."""
    return PaymentAnalytics()


# Test data constants
TEST_VALID_PROVINCES = [
    "Jawa Barat", "Jawa Tengah", "Jawa Timur",
    "Sumatera Utara", "DKI Jakarta", "Bali"
]

TEST_VALID_YEARS = [2020, 2021, 2022, 2023, 2024]

TEST_SAMPLE_PRODUCT = "Laptop"

TEST_SAMPLE_CATEGORY = "Elektronik"

TEST_SAMPLE_PAYMENT = "debit"
