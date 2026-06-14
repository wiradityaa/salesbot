import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------------
# System prompt
# -------------------------------------------------------

SYSTEM_PROMPT = """Kamu adalah SalesBot, asisten analitik penjualan retail untuk toko di Jawa.

Tugasmu: ubah data analitik mentah menjadi jawaban bahasa Indonesia yang jelas dan informatif.

ATURAN KETAT:
1. Gunakan HANYA angka dari data yang diberikan - JANGAN mengubah atau mengarang angka
2. Tulis dalam bahasa Indonesia yang natural dan profesional
3. Maksimal 3-4 paragraf atau 8 poin bullet
4. Selalu sebutkan angka spesifik (revenue, profit, units) jika tersedia di data
5. Akhiri dengan 1 insight atau rekomendasi singkat jika relevan
6. Jika data kosong, katakan data tidak tersedia untuk filter tersebut
7. Format angka rupiah dengan Rp dan titik sebagai thousand separator (contoh: Rp 1.250.000)

JANGAN:
- Mengarang data yang tidak ada di input
- Memberikan saran yang tidak didukung data
- Menggunakan bahasa terlalu formal atau kaku"""


# -------------------------------------------------------
# Generate response
# -------------------------------------------------------

def generate_response(user_query: str, analytics_data: dict,
                       intent_data: dict, conversation_context: str = "") -> str:
    """
    Generate jawaban natural language dari data analytics.
    LLM hanya bertugas menulis - tidak boleh mengubah angka.
    
    Args:
        user_query: Pertanyaan user
        analytics_data: Hasil dari analytics/recommendation tools
        intent_data: Intent classification hasil
        conversation_context: (Optional) Konteks percakapan sebelumnya untuk multi-turn
    """
    if analytics_data.get("status") == "out_of_scope":
        return (
            "Maaf, pertanyaan tersebut di luar cakupan sistem analitik penjualan ini. "
            "Saya hanya dapat menjawab pertanyaan seputar data penjualan retail "
            "di 6 provinsi Jawa - produk, kategori, provinsi, tren waktu, "
            "metode pembayaran, dan rekomendasi strategi."
        )

    if analytics_data.get("status") == "error":
        return (
            f"Terjadi kesalahan saat mengambil data: {analytics_data.get('error', 'Unknown error')}. "
            "Silakan coba lagi atau hubungi administrator."
        )

    # Siapkan context untuk LLM
    data_preview = analytics_data.get("data", [])

    # Batasi data yang dikirim ke LLM — maksimal 20 baris
    if isinstance(data_preview, list):
        data_preview = data_preview[:20]
    elif isinstance(data_preview, dict):
        # Untuk general_summary yang nested
        for key in data_preview:
            if isinstance(data_preview[key], list):
                data_preview[key] = data_preview[key][:10]

    # Include conversation context jika tersedia
    conversation_section = ""
    if conversation_context:
        conversation_section = f"""
Konteks percakapan sebelumnya:
{conversation_context}

"""

    context = f"""
{conversation_section}Pertanyaan user: {user_query}

Intent terdeteksi: {intent_data.get('intent', 'unknown')}
Filter aktif:
- Provinsi : {intent_data.get('province') or 'Semua provinsi'}
- Kategori : {intent_data.get('category') or 'Semua kategori'}
- Tahun    : {intent_data.get('year') or 'Semua tahun'}
- Metrik   : {intent_data.get('metric') or 'default'}

Data analitik:
{json.dumps(data_preview, ensure_ascii=False, indent=2, default=str)}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": context}
            ],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "Maaf, terjadi kesalahan saat memproses jawaban. "
            f"Detail: {str(e)}"
        )