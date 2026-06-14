# SalesBot

SalesBot adalah proyek analitik data penjualan berbasis Python dan PostgreSQL/Supabase. Proyek ini bertujuan mengubah data transaksi mentah menjadi insight bisnis yang dapat diakses melalui modul analytics, dashboard, dan chatbot berbasis LLM.

## Progress Saat Ini

Bagian yang sudah dikerjakan:

- Dataset penjualan mentah dan hasil pembersihan.
- Star schema PostgreSQL untuk data penjualan.
- Pipeline ETL untuk validasi, pembersihan, transformasi, dan pemuatan data.
- Fallback penyimpanan cleaned dataset ketika koneksi database gagal.
- Koneksi dan helper query ke Supabase PostgreSQL.
- Analytics berdasarkan produk, provinsi, kategori, tren waktu, dan metode pembayaran.
- Recommendation engine berbasis rule untuk produk, provinsi, dan kategori.
- AI agent untuk klasifikasi intent, routing tools, dan pembuatan jawaban natural.
- Pipeline SalesBot end-to-end menggunakan Groq.
- **Dashboard interaktif dengan visualisasi real-time** (Revenue per provinsi, kategori, tren bulanan, KPI cards).
- **Halaman chat SalesBot** dengan AI Agent untuk Q&A berbasis data penjualan.
- **UI components** (charts dan KPI cards) untuk reusability.
- **Chat history persistence** - Percakapan disimpan ke file dan dapat dimuat kembali.
- **Multi-turn conversation support** - AI Agent mempertimbangkan konteks percakapan sebelumnya.
- **29 evaluation test questions** untuk mengevaluasi kualitas SalesBot.
- **Evaluation pipeline** untuk mengukur intent accuracy, relevance, dan performance metrics.
- **Automated testing suite** - 31 test cases untuk analytics, 15+ test cases untuk recommendation engine dengan pytest.
- **Test documentation** - Comprehensive test documentation di test_log/README.md.

Bagian yang belum dikerjakan:

- Migration script untuk reset database.
- Dokumentasi deployment dan infrastructure setup.

## Fitur Analytics

| Modul | Fitur |
| --- | --- |
| Product Analytics | Top produk, performa produk, dan detail produk |
| Province Analytics | Revenue, perbandingan, produk unggulan, dan tren per provinsi |
| Category Analytics | Revenue kategori, distribusi kategori, dan produk unggulan |
| Trend Analytics | Tren bulanan, kuartalan, tahunan, serta bulan terbaik dan terburuk |
| Payment Analytics | Revenue, distribusi, dan tren metode pembayaran |

## Recommendation Engine

| Fitur | Kegunaan |
| --- | --- |
| Product Quadrant | Mengelompokkan produk menjadi Stars, Cash Cows, Question Marks, dan Dogs berdasarkan median volume dan profit |
| Province Recommendation | Membandingkan revenue dan profit provinsi terhadap rata-rata nasional lalu memberikan rekomendasi |
| Category Recommendation | Menentukan kategori yang perlu diprioritaskan, dipertahankan, atau dievaluasi berdasarkan margin |

## AI Agent

Pipeline SalesBot memproses pertanyaan pengguna melalui tiga tahap:

1. `classify_intent()` mengubah pertanyaan menjadi intent dan filter terstruktur menggunakan Groq.
2. `route()` memilih analytics tool atau recommendation tool yang sesuai.
3. `generate_response()` mengubah hasil analitik menjadi jawaban bahasa Indonesia.

Intent yang didukung meliputi analisis produk, provinsi, kategori, tren, metode pembayaran, rekomendasi, ringkasan umum, dan pertanyaan di luar cakupan.

## Tech Stack

- Python
- pandas
- NumPy
- PostgreSQL / Supabase
- psycopg2
- LangChain
- Groq
- Streamlit
- Plotly
- pytest (untuk automated testing)
- pytest-cov (untuk coverage report)

## Setup

1. Buat virtual environment.

```bash
python -m venv .venv
```

2. Aktifkan virtual environment.

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Linux atau macOS:

```bash
source .venv/bin/activate
```

3. Instal dependencies.

```bash
pip install -r requirements.txt
```

4. Salin `.env.example` menjadi `.env`, kemudian isi konfigurasi berikut:

```env
SUPABASE_HOST=your-project-id.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_database_password_here
GROQ_API_KEY=your_groq_api_key_here
```

5. Jalankan `etl/schema.sql` pada PostgreSQL/Supabase.

6. Jalankan pipeline ETL.

```bash
python etl/etl_pipeline.py
```

Jika koneksi database gagal, hasil transformasi akan disimpan ke:

```text
data/DatasetPenjualanToko_cleaned.csv
```

## Contoh Penggunaan

```python
from analytics import ProductAnalytics, ProvinceAnalytics

product_analytics = ProductAnalytics()
province_analytics = ProvinceAnalytics()

top_products = product_analytics.top_products_by_revenue(
    limit=5,
    province="Jawa Tengah",
    year=2023,
)

province_comparison = province_analytics.province_comparison(year=2023)
```

Contoh menggunakan recommendation engine:

```python
from recommendation import classify_product_quadrants, recommend_by_province

product_quadrants = classify_product_quadrants(province="Jawa Barat", year=2023)
province_recommendations = recommend_by_province(year=2023)
```

Contoh menjalankan pipeline SalesBot:

```python
from agents import run_pipeline

result = run_pipeline("Top 5 produk terlaris di Jawa Barat tahun 2023")

print(result["answer"])
print(result["intent_data"])
print(result["raw_data"])
```

Hasil query analytics menggunakan format:

```python
{
    "status": "success",
    "data": [],
    "row_count": 0,
    "error": None,
}
```

## Evaluasi SalesBot

Jalankan evaluation pipeline untuk menilai kualitas SalesBot:

```bash
python evaluation/evaluate.py
```

**Metrics yang diukur:**
- **Intent Accuracy**: Berapa persen AI mengenali intent dengan benar
- **Relevance Score**: Apakah jawaban memuat keywords yang diharapkan
- **Language Quality**: Kualitas bahasa Indonesia yang digunakan
- **Completeness**: Apakah jawaban cukup lengkap
- **Clarity**: Kejelasan penyajian informasi
- **Latency**: Kecepatan processing (ms)

**Output:**
- Detailed report: `evaluation/reports/eval_report_YYYYMMDD_HHMMSS.json`
- Summary metrics printed to console
- History tracking semua evaluation runs

Contoh hasil evaluation:

```text
SALESBOT EVALUATION REPORT

Total Questions Tested: 29
Successful Runs: 29
Failed Runs: 0

QUALITY METRICS
Intent Accuracy: 95.2%
Avg Relevance Score: 0.87/1.0
Avg Language Quality: 0.98/1.0
Avg Completeness: 0.91/1.0
Avg Clarity: 0.95/1.0

PERFORMANCE METRICS
Avg Latency: 2840ms
```

## Automated Testing

### Running Tests dengan Pytest

Jalankan automated tests untuk verifikasi analytics dan recommendation modules:

```bash
# Run semua tests
python -m pytest test_log/ -v

# Run analytics tests saja
python -m pytest test_log/test_analytics.py -v

# Run recommendation tests saja
python -m pytest test_log/test_recommendation.py -v

# Run dengan coverage report
python -m pytest test_log/ -v --cov=analytics --cov=recommendation --cov-report=html
```

### Test Coverage

**Analytics Tests:** 31 test cases
- ProductAnalytics: 8 tests
- ProvinceAnalytics: 6 tests
- CategoryAnalytics: 4 tests
- TrendAnalytics: 6 tests
- PaymentAnalytics: 4 tests
- Analytics Integration: 3 tests

**Recommendation Tests:** 15+ test cases
- Product Quadrants: 4 tests
- Province Recommendation: 4 tests
- Category Recommendation: 3 tests
- Recommendation Integration: 4+ tests

### Test Fixtures

Tests menggunakan pytest fixtures untuk efficient setup:

```python
@pytest.fixture
def product_analytics       # ProductAnalytics instance
def province_analytics      # ProvinceAnalytics instance
def category_analytics      # CategoryAnalytics instance
def trend_analytics         # TrendAnalytics instance
def payment_analytics       # PaymentAnalytics instance
```

Lihat `test_log/README.md` untuk dokumentasi testing lebih lengkap.

## Menjalankan UI Streamlit

Setelah setup selesai, jalankan aplikasi Streamlit dengan:

```bash
streamlit run ui/app.py
```

Aplikasi akan membuka di browser pada `http://localhost:8501`.

### Halaman yang Tersedia:

1. **Home** (`ui/app.py`)
   - Hero section dan feature overview
   - Navigasi ke Dashboard dan SalesBot Chat

2. **Dashboard** (`ui/pages/1_Dashboard.py`)
   - KPI cards dengan metrik utama
   - Revenue by Province (grafik interaktif)
   - Revenue by Category (grafik interaktif)
   - Monthly Trend (grafik tren penjualan)

3. **SalesBot Chat** (`ui/pages/2_SalesBot.py`)
   - Chat interface untuk Q&A berbasis data
   - Proses natural language menggunakan AI Agent
   - Jawaban terstruktur dengan insight otomatis
   - Quick question buttons untuk pertanyaan umum

## Chat History & Multi-turn Conversation

Chat history otomatis disimpan ke `data/chat_history/conversations.json`. Setiap percakapan tersimpan dengan:
- Unique conversation ID
- Timestamp (created_at dan updated_at)
- Semua messages (user dan assistant)

**Fitur:**
- Sidebar menampilkan daftar recent conversations
- Klik conversation untuk memuat ulang history
- Delete individual conversation dengan tombol 🗑
- Multi-turn awareness: AI Agent mempertimbangkan konteks percakapan sebelumnya
- Clear Chat untuk reset session saat ini tanpa menghapus file

## TODO

### Data dan Database

- [x] Menyiapkan dataset penjualan.
- [x] Membersihkan dan mentransformasi dataset.
- [x] Membuat star schema PostgreSQL.
- [x] Membuat pipeline ETL.
- [x] Membuat koneksi Supabase PostgreSQL.
- [ ] Menambahkan migration atau proses reset database.
- [ ] Menambahkan validasi kualitas data yang lebih lengkap.

### Analytics

- [x] Membuat product analytics.
- [x] Membuat province analytics.
- [x] Membuat category analytics.
- [x] Membuat trend analytics.
- [x] Membuat payment analytics.
- [ ] Menambahkan validasi parameter analytics.
- [x] Menambahkan automated test untuk seluruh query analytics.
- [ ] Menambahkan logging dan error handling yang lebih spesifik.

### Recommendation dan AI Agent

- [x] Membuat recommendation engine berbasis rule.
- [x] Membuat klasifikasi kuadran produk.
- [x] Membuat rekomendasi provinsi dan kategori.
- [x] Membuat intent classifier.
- [x] Membuat tools untuk mengakses analytics dan recommendation.
- [x] Membuat tool router.
- [x] Mengintegrasikan Groq.
- [x] Membuat response generator.
- [x] Membuat pipeline SalesBot end-to-end.
- [x] Menambahkan percakapan multi-turn dan penyimpanan riwayat chat.
- [x] Menambahkan automated test untuk recommendation dan AI agent.

### UI dan Evaluation

- [x] Membuat dashboard Streamlit.
- [x] Membuat KPI cards dan charts.
- [x] Membuat halaman chat SalesBot.
- [x] Menambahkan percakapan multi-turn dan penyimpanan riwayat chat.
- [x] Menambahkan kumpulan pertanyaan evaluasi (test_questions.json).
- [x] Membuat evaluation pipeline.
- [ ] Menambahkan dokumentasi deployment.

## Project Structure

Keterangan:

- `[done]`: sudah tersedia.
- `[todo]`: direncanakan dan belum tersedia.

```text
salesbot/
|-- data/
|   |-- DatasetPenjualanToko.csv                 [done]
|   `-- DatasetPenjualanToko_cleaned.csv         [done]
|-- etl/
|   |-- etl_pipeline.py                          [done]
|   `-- schema.sql                               [done]
|-- analytics/
|   |-- __init__.py                              [done]
|   |-- db_utils.py                              [done]
|   |-- product_analytics.py                     [done]
|   |-- province_analytics.py                    [done]
|   |-- category_analytics.py                    [done]
|   |-- trend_analytics.py                       [done]
|   `-- payment_analytics.py                     [done]
|-- recommendation/
|   |-- __init__.py                              [done]
|   `-- recommender.py                           [done]
|-- agents/
|   |-- __init__.py                              [done]
|   |-- intent_classifier.py                     [done]
|   |-- tool_router.py                           [done]
|   |-- tools.py                                 [done]
|   `-- response_generator.py                    [done]
|-- ui/
|   |-- app.py                                   [done]
|   |-- chat_manager.py                          [done]
|   |-- pages/
|   |   |-- 1_Dashboard.py                       [done]
|   |   `-- 2_SalesBot.py                        [done]
|   `-- components/
|       |-- kpi_cards.py                         [done]
|       `-- charts.py                            [done]
|-- evaluation/
|   |-- test_questions.json                      [done]
|   |-- evaluate.py                              [done]
|   `-- reports/                                 [auto-generated]
|-- test_log/
|   |-- conftest.py                              [done]
|   |-- test_analytics.py                        [done]
|   |-- test_recommendation.py                   [done]
|   `-- README.md                                [done]
|-- .streamlit/
|   `-- secrets.toml                             [todo, gitignored]
|-- requirements.txt                             [done]
|-- .env                                         [done, gitignored]
|-- .env.example                                 [done]
|-- .gitignore                                   [done]
`-- README.md                                    [done]
```

## Security

- Jangan commit `.env` atau `.streamlit/secrets.toml`.
- Gunakan `.env.example` sebagai template konfigurasi.
- Simpan database credentials dan API key sebagai environment variables.
