import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------------
# System prompt
# -------------------------------------------------------

SYSTEM_PROMPT = """Kamu adalah intent classifier untuk sistem analitik penjualan retail di Jawa.
Tugasmu adalah menganalisis pertanyaan user dan mengembalikan JSON terstruktur.

INTENT yang tersedia:
- product_analysis    : pertanyaan tentang produk, performa produk, top produk
- province_analysis   : pertanyaan tentang provinsi, wilayah, daerah
- category_analysis   : pertanyaan tentang kategori produk
- trend_analysis      : pertanyaan tentang tren waktu, bulanan, tahunan, pertumbuhan
- payment_analysis    : pertanyaan tentang metode pembayaran
- recommendation      : pertanyaan meminta rekomendasi, saran, strategi
- general_summary     : pertanyaan umum tentang ringkasan bisnis keseluruhan
- out_of_scope        : pertanyaan di luar konteks penjualan retail

PROVINSI yang valid: Jawa Barat, Jawa Tengah, Jawa Timur, DKI Jakarta, Banten, DI Yogyakarta

KATEGORI yang valid: Snacks, Instant Noodles, Personal Care, Health, Groceries, Smokes, Drinks

Kembalikan HANYA JSON dengan format ini, tanpa teks lain:
{
  "intent": "<salah satu intent di atas>",
  "metric": "<revenue|profit|units|margin|null>",
  "province": "<nama provinsi valid atau null>",
  "category": "<nama kategori valid atau null>",
  "product": "<nama produk spesifik atau null>",
  "year": <tahun integer atau null>,
  "limit": <integer jumlah top-N atau null>,
  "confidence": <0.0 sampai 1.0>
}

CONTOH:

Input: "produk apa yang paling laris?"
Output: {"intent":"product_analysis","metric":"units","province":null,"category":null,"product":null,"year":null,"limit":5,"confidence":0.95}

Input: "bagaimana performa penjualan di Jawa Barat?"
Output: {"intent":"province_analysis","metric":"revenue","province":"Jawa Barat","category":null,"product":null,"year":null,"limit":null,"confidence":0.97}

Input: "tren revenue bulan per bulan tahun 2023"
Output: {"intent":"trend_analysis","metric":"revenue","province":null,"category":null,"product":null,"year":2023,"limit":null,"confidence":0.96}

Input: "kategori mana yang paling menguntungkan di Jawa Timur?"
Output: {"intent":"category_analysis","metric":"profit","province":"Jawa Timur","category":null,"product":null,"year":null,"limit":null,"confidence":0.94}

Input: "berikan rekomendasi produk mana yang harus difokuskan"
Output: {"intent":"recommendation","metric":null,"province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.93}

Input: "berapa total revenue keseluruhan?"
Output: {"intent":"general_summary","metric":"revenue","province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.95}

Input: "siapa presiden Indonesia?"
Output: {"intent":"out_of_scope","metric":null,"province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.99}

Input: "top 10 produk terlaris di Banten tahun 2024"
Output: {"intent":"product_analysis","metric":"units","province":"Banten","category":null,"product":null,"year":2024,"limit":10,"confidence":0.98}

Input: "perbandingan semua provinsi dari sisi profit"
Output: {"intent":"province_analysis","metric":"profit","province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.96}

Input: "metode pembayaran apa yang paling sering digunakan?"
Output: {"intent":"payment_analysis","metric":"units","province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.95}

Input: "apakah Snacks lebih untung dari Drinks?"
Output: {"intent":"category_analysis","metric":"profit","province":null,"category":null,"product":null,"year":null,"limit":null,"confidence":0.92}"""


# -------------------------------------------------------
# Classify intent
# -------------------------------------------------------

def classify_intent(user_query: str) -> dict:
    """
    Klasifikasi intent dari user query.
    Return dict dengan intent, metric, province, category, product, year, limit, confidence.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_query}
            ],
            temperature=0.0,    # deterministic
            max_tokens=200
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown fences kalau ada
        raw = raw.replace("```json", "").replace("```", "").strip()

        intent_data = json.loads(raw)

        # Validasi field wajib ada
        required_fields = ["intent", "metric", "province", "category",
                           "product", "year", "limit", "confidence"]
        for field in required_fields:
            if field not in intent_data:
                intent_data[field] = None

        return {"status": "success", "data": intent_data, "error": None}

    except json.JSONDecodeError as e:
        return {    
            "status": "error",
            "data": _fallback_intent(),
            "error": f"JSON parse error: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": _fallback_intent(),
            "error": str(e)
        }


def _fallback_intent() -> dict:
    """Fallback intent kalau classifier gagal."""
    return {
        "intent": "general_summary",
        "metric": "revenue",
        "province": None,
        "category": None,
        "product": None,
        "year": None,
        "limit": None,
        "confidence": 0.0
    }