# SalesBot Testing Documentation

## Overview

Dokumen ini berisi pengujian untuk sistem **SalesBot**, mencakup:

* ETL Pipeline Testing (legacy)
* Analytics Engine Automated Testing (pytest)
* Recommendation Engine Automated Testing (pytest)
* End-to-End Pipeline Testing (legacy)

Tujuan pengujian adalah memastikan bahwa:

* Data berhasil diekstrak, ditransformasi, dan dimuat ke database.
* Query analytics berjalan dengan benar untuk semua modul.
* Recommendation engine memberikan output yang valid.
* Pipeline NLP → Analytics → Response Generator berfungsi sesuai intent yang terdeteksi.

---

# 1. Automated Testing dengan Pytest

## Setup

### Install pytest

```bash
pip install pytest pytest-cov
```

### Struktur Test Files

```text
test_log/
├── conftest.py                 # Pytest fixtures dan setup
├── test_analytics.py           # Test suite untuk analytics modules
├── test_recommendation.py       # Test suite untuk recommendation engine
└── README.md                   # Documentation ini
```

## Running Tests

### Run semua tests

```bash
pytest test_log/ -v
```

### Run tests untuk analytics saja

```bash
pytest test_log/test_analytics.py -v
```

### Run tests untuk recommendation saja

```bash
pytest test_log/test_recommendation.py -v
```

### Run tests dengan coverage report

```bash
pytest test_log/ -v --cov=analytics --cov=recommendation --cov-report=html
```

### Run specific test class

```bash
pytest test_log/test_analytics.py::TestProductAnalytics -v
```

### Run specific test

```bash
pytest test_log/test_analytics.py::TestProductAnalytics::test_top_products_by_revenue_returns_list -v
```

## Test Coverage

### Analytics Test Suite (`test_analytics.py`)

Total: **6 test classes, 30+ test cases**

| Module | Tests |
| --- | --- |
| ProductAnalytics | 8 tests |
| ProvinceAnalytics | 6 tests |
| CategoryAnalytics | 4 tests |
| TrendAnalytics | 6 tests |
| PaymentAnalytics | 4 tests |
| Analytics Integration | 3 tests |

**Test Categories:**
- ✅ Return type validation (mengembalikan dict/list)
- ✅ Data structure validation
- ✅ Filter parameter testing (province, year, limit)
- ✅ Edge case testing
- ✅ Integration testing (multiple queries sequential)

### Recommendation Test Suite (`test_recommendation.py`)

Total: **4 test classes, 15+ test cases**

| Module | Tests |
| --- | --- |
| Product Quadrants | 4 tests |
| Province Recommendation | 4 tests |
| Category Recommendation | 3 tests |
| Recommendation Integration | 4+ tests |

**Test Categories:**
- ✅ Return type validation
- ✅ Multi-year testing
- ✅ Consistency testing (same input → same output)
- ✅ Format validation

## Test Fixtures (`conftest.py`)

Fixtures yang tersedia:

```python
@pytest.fixture
def product_analytics()      # ProductAnalytics instance
def province_analytics()     # ProvinceAnalytics instance
def category_analytics()     # CategoryAnalytics instance
def trend_analytics()        # TrendAnalytics instance
def payment_analytics()      # PaymentAnalytics instance
```

## Expected Test Results

Ketika semua tests pass, output akan terlihat seperti:

```
test_log/test_analytics.py::TestProductAnalytics::test_top_products_by_revenue_returns_list PASSED [  5%]
test_log/test_analytics.py::TestProductAnalytics::test_top_products_with_valid_limit PASSED [ 10%]
...
test_log/test_recommendation.py::TestProductQuadrants::test_classify_product_quadrants_returns_dict PASSED [ 85%]
...

======= 45 passed in 15.23s =======
```

## Interpreting Test Results

### PASSED ✅
Test berhasil dan output sesuai ekspektasi.

### FAILED ❌
Test gagal. Lihat error message untuk details.

### ERROR
Error saat setup atau teardown test.

---

# 2. ETL Pipeline Testing (Legacy)

## File Terkait

```text
etl_pipeline.py
Output ETL.log
```

## Tujuan

Memastikan proses berikut berjalan tanpa error:

```text
CSV Dataset
    ↓
Cleaning & Transformation
    ↓
Dimension Loading
    ↓
Fact Loading
    ↓
Verification
```

## Hasil Pengujian

### Dataset

| Parameter      | Nilai           |
| -------------- | --------------- |
| Total Rows     | 200.000         |
| Total Columns  | 11              |
| Missing Value  | Tidak ditemukan |
| Duplicate Rows | 0               |

### Data Quality Check

Ditemukan:

```text
7.927 baris Revenue mismatch
```

Issue ini berasal dari kualitas data sumber dan tidak menghentikan proses ETL.

### Loading Result

| Table        | Rows    |
| ------------ | ------- |
| dim_date     | 731     |
| dim_product  | 20      |
| dim_location | 97      |
| dim_payment  | 2       |
| fact_sales   | 200.000 |

### Verification

```text
Expected Rows : 200000
Actual Rows   : 200000
Status        : OK
```

### Status

```text
PASS
```

### Kesimpulan

ETL berhasil dijalankan hingga selesai dan seluruh data berhasil dimuat ke database.

---

# 2. Analytics Engine Test

## File Terkait

```text
test_analytics.py
Output Test Analytics.log
```

## Tujuan

Memastikan seluruh SQL query analytics dapat dieksekusi dan menghasilkan data yang valid.

## Query yang Diuji

```python
top_products_by_revenue()
top_products_by_units()
product_performance_summary()

revenue_by_province()
top_products_in_province()

revenue_by_category()
category_by_province()

monthly_revenue()
quarterly_revenue()
year_over_year()

revenue_by_payment()
payment_by_province()
```

## Hasil Pengujian

| Analytics Function          | Status |
| --------------------------- | ------ |
| top_products_by_revenue     | PASS   |
| top_products_by_units       | PASS   |
| product_performance_summary | PASS   |
| revenue_by_province         | PASS   |
| top_products_in_province    | PASS   |
| revenue_by_category         | PASS   |
| category_by_province        | PASS   |
| monthly_revenue             | PASS   |
| quarterly_revenue           | PASS   |
| year_over_year              | PASS   |
| revenue_by_payment          | PASS   |
| payment_by_province         | PASS   |

### Summary

```text
12 / 12 TESTS PASSED
```

### Kesimpulan

Seluruh query analytics berhasil dijalankan dan menghasilkan output yang valid.

---

# 3. Pipeline Integration Test

## File Terkait

```text
test_pipeline.py
Output Test Queries.log
```

## Tujuan

Menguji alur lengkap sistem:

```text
User Query
    ↓
Intent Detection
    ↓
Analytics Layer
    ↓
Response Generation
```

## Query Pengujian

```text
produk apa yang paling laris?
bagaimana performa penjualan di Jawa Barat?
kategori mana yang paling menguntungkan?
tren revenue per bulan tahun 2023
metode pembayaran apa yang paling banyak digunakan?
berikan rekomendasi produk yang harus difokuskan
berapa total revenue keseluruhan?
siapa presiden Indonesia?
```

---

## Hasil Pengujian

### 1. Product Analysis

**Query**

```text
produk apa yang paling laris?
```

**Hasil**

```text
Intent     : product_analysis
Confidence : 0.95
```

**Status:** PASS

Pipeline berhasil memberikan ranking produk terlaris berdasarkan data penjualan.

---

### 2. Province Analysis

**Query**

```text
bagaimana performa penjualan di Jawa Barat?
```

**Hasil**

```text
Intent     : province_analysis
Confidence : 0.97
```

**Status:** PASS

Pipeline berhasil menghasilkan analisis performa penjualan berdasarkan provinsi.

---

### 3. Category Analysis

**Query**

```text
kategori mana yang paling menguntungkan?
```

**Hasil**

```text
Intent     : category_analysis
Confidence : 0.94
```

**Status:** PASS

Pipeline berhasil mengidentifikasi kategori produk dengan profit tertinggi.

---

### 4. Trend Analysis

**Query**

```text
tren revenue per bulan tahun 2023
```

**Hasil**

```text
Intent     : trend_analysis
Confidence : 0.96
```

**Status:** PASS

Pipeline berhasil menghasilkan analisis tren revenue bulanan.

---

### 5. Payment Analysis

**Query**

```text
metode pembayaran apa yang paling banyak digunakan?
```

**Status:** FAIL

Error yang ditemukan:

```text
Database connection timeout
```

Kemungkinan penyebab:

* Koneksi internet tidak stabil
* Latensi server database
* Limit koneksi PostgreSQL/Supabase

Perlu dilakukan pengujian ulang.

---

### 6. Recommendation Engine

**Query**

```text
berikan rekomendasi produk yang harus difokuskan
```

**Status:** PARTIAL PASS

Intent berhasil dikenali, namun sistem belum dapat menghasilkan rekomendasi yang memadai karena data pendukung yang diperlukan belum tersedia.

---

### 7. General Summary

**Query**

```text
berapa total revenue keseluruhan?
```

**Status:** PASS

Pipeline berhasil menghasilkan ringkasan revenue keseluruhan.

---

### 8. Out-of-Scope Detection

**Query**

```text
siapa presiden Indonesia?
```

**Hasil**

```text
Intent     : out_of_scope
Confidence : 0.99
```

**Status:** PASS

Sistem berhasil mendeteksi pertanyaan di luar domain analitik penjualan dan memberikan respons yang sesuai.

---

# Overall Testing Summary

| Component              | Result                    |
| ---------------------- | ------------------------- |
| ETL Pipeline           | PASS                      |
| Database Loading       | PASS                      |
| Analytics Queries      | PASS (12/12)              |
| Intent Classification  | PASS                      |
| Response Generation    | PASS                      |
| Out-of-Scope Detection | PASS                      |
| Payment Analysis Query | FAIL (Connection Timeout) |
| Recommendation Module  | PARTIAL                   |

---

# Current Readiness Assessment

| Module                | Status            |
| --------------------- | ----------------- |
| ETL Layer             | READY             |
| Analytics Layer       | READY             |
| Intent Detection      | READY             |
| Response Generation   | READY             |
| Recommendation Engine | NEEDS IMPROVEMENT |
| Database Connectivity | NEEDS RETESTING   |

---

# Conclusion

Berdasarkan hasil pengujian sementara:

* ETL berhasil memproses dan memuat **200.000 transaksi** ke data warehouse.
* Seluruh query analytics berhasil dijalankan (**12/12 PASS**).
* Pipeline NLP dan analytics mampu menangani berbagai jenis pertanyaan bisnis dengan confidence di atas 0.93.
* Sistem mampu mendeteksi pertanyaan di luar domain penjualan dengan baik.
* Masih diperlukan peningkatan pada modul rekomendasi dan pengujian ulang stabilitas koneksi database untuk menghindari timeout pada query tertentu.

Secara keseluruhan, sistem telah siap digunakan untuk demonstrasi dan tahap pengembangan lanjutan dengan beberapa perbaikan minor pada reliability dan recommendation engine.
