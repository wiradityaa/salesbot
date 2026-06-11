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

Bagian yang belum dikerjakan:

- Automated testing.
- Dashboard dan halaman chat SalesBot.
- Evaluation pipeline.
- Deployment.

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
- [ ] Menambahkan automated test untuk seluruh query analytics.
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
- [ ] Menambahkan percakapan multi-turn dan penyimpanan riwayat chat.
- [ ] Menambahkan automated test untuk recommendation dan AI agent.

### UI dan Evaluation

- [ ] Membuat dashboard Streamlit.
- [ ] Membuat KPI cards dan charts.
- [ ] Membuat halaman chat SalesBot.
- [ ] Membuat kumpulan pertanyaan evaluasi.
- [ ] Membuat evaluation pipeline.
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
|   |-- app.py                                   [todo]
|   |-- pages/
|   |   |-- 1_Dashboard.py                       [todo]
|   |   `-- 2_SalesBot.py                        [todo]
|   `-- components/
|       |-- kpi_cards.py                         [todo]
|       `-- charts.py                            [todo]
|-- evaluation/
|   |-- test_questions.json                      [todo]
|   `-- evaluate.py                              [todo]
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
