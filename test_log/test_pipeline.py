# test_pipeline.py — hapus setelah selesai

from agents import run_pipeline

test_queries = [
    "produk apa yang paling laris?",
    "bagaimana performa penjualan di Jawa Barat?",
    "kategori mana yang paling menguntungkan?",
    "tren revenue per bulan tahun 2023",
    "metode pembayaran apa yang paling banyak digunakan?",
    "berikan rekomendasi produk yang harus difokuskan",
    "berapa total revenue keseluruhan?",
    "siapa presiden Indonesia?",
]

print("=" * 60)
print("SalesBot Pipeline: Test Queries")
print("=" * 60)

for query in test_queries:
    print(f"\nQ: {query}")
    print("-" * 40)
    result = run_pipeline(query)
    print(f"Intent : {result['intent_data'].get('intent')} "
          f"(conf: {result['intent_data'].get('confidence')})")
    print(f"Answer : {result['answer'][:200]}...")
    print()