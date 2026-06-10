import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------
# Connection
# -------------------------------------------------------

def get_connection():
    """Buat koneksi ke Supabase PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("SUPABASE_HOST"),
        port=int(os.getenv("SUPABASE_PORT")),
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        sslmode="require",
        connect_timeout=10
    )

# -------------------------------------------------------
# Query helper
# -------------------------------------------------------

def execute_query(sql: str, params: tuple = None) -> dict:
    """
    Eksekusi SELECT query, return dict standar.
    Return format: {status, data, row_count, error}
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            data = [dict(r) for r in rows]
        return {
            "status": "success",
            "data": data,
            "row_count": len(data),
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": [],
            "row_count": 0,
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()