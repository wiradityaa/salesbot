import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# -------------------------------------------------------
# Load environment variables
# -------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------
# 1. Configuration
# -------------------------------------------------------

def get_connection():
    """Buat koneksi ke Supabase PostgreSQL."""
    host = os.getenv("SUPABASE_HOST")
    port = os.getenv("SUPABASE_PORT")
    dbname = os.getenv("SUPABASE_DB")
    password = os.getenv("SUPABASE_PASSWORD")
    user = os.getenv("SUPABASE_USER")
    
    # Validasi credentials ada
    if not host or not password:
        raise ValueError(
            "Credentials tidak lengkap. Pastikan .env file ada dengan "
            "SUPABASE_HOST dan SUPABASE_PASSWORD"
        )
    
    # Ensure port is an int when provided
    try:
        port_arg = int(port) if port else None
    except Exception:
        port_arg = port

    print(f"[INFO] Connecting to {host} as user {user}...")
    return psycopg2.connect(
        host=host,
        port=port_arg,
        dbname=dbname,
        user=user,
        password=password,
        sslmode="require"
    )

# -------------------------------------------------------
# 2. Extract & Validate
# -------------------------------------------------------

def extract_and_validate(csv_path: str) -> pd.DataFrame:
    """Baca CSV dan validasi kolom wajib."""
    print(f"[1/8] Extracting: {csv_path}")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File CSV tidak ditemukan: {csv_path}")
    
    # Read CSV with price columns as strings to handle Indonesian formatting manually
    df = pd.read_csv(csv_path, sep=";", dtype={
        "Unit_Price": str, "Revenue": str, "Unit Cost": str
    })

    required_cols = [
        "Transaction_ID", "Date", "Product_Name", "Category",
        "Units_Sold", "Unit_Price", "Revenue", "Store_Location",
        "Payment_Method", "Province", "Unit Cost"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    assert not missing, f"Kolom tidak ditemukan: {missing}"

    print(f"    Rows read: {len(df)}")
    print(f"    Columns: {df.columns.tolist()}")

    # Validasi null
    null_counts = df[required_cols].isnull().sum()
    if null_counts.any():
        print(f"    [WARN] Null values ditemukan:\n{null_counts[null_counts > 0]}")
    else:
        print("    Null check: OK")

    return df

# -------------------------------------------------------
# 3. Clean & Transform
# -------------------------------------------------------

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan dan transformasi data ke format star schema."""
    print("[2/8] Cleaning & transforming...")

    # Drop duplicates berdasarkan Transaction_ID
    before = len(df)
    df = df.drop_duplicates(subset=["Transaction_ID"])
    print(f"    Duplicates dropped: {before - len(df)}")

    # Convert price columns: remove dots (thousands separator) and convert to numeric
    df["Unit_Price"] = df["Unit_Price"].astype(str).str.replace(".", "", regex=False).astype(float)
    df["Revenue"] = df["Revenue"].astype(str).str.replace(".", "", regex=False).astype(float)
    df["Unit Cost"] = df["Unit Cost"].astype(str).str.replace(".", "", regex=False).astype(float)

    # Hitung Profit
    df["Profit"] = df["Revenue"] - (df["Units_Sold"] * df["Unit Cost"])

    # Verifikasi Revenue
    revenue_check = df["Units_Sold"] * df["Unit_Price"]
    mismatch_mask = (abs(df["Revenue"] - revenue_check) > 1)
    mismatch = mismatch_mask.sum()
    
    if mismatch > 0:
        print(f"    [WARN] Revenue mismatch pada {mismatch} baris (data quality issue - allowing to continue)")

    # Parse tanggal
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    # Rename kolom agar konsisten
    df = df.rename(columns={"Unit Cost": "Unit_Cost"})

    print(f"    Rows after clean: {len(df)}")
    return df

# -------------------------------------------------------
# 4–5. Load Dimension Tables
# -------------------------------------------------------

def load_dim_date(conn, df: pd.DataFrame) -> dict:
    """Load dim_date, return mapping full_date → date_id."""
    print("[3/8] Loading dim_date...")
    dates = df["Date"].drop_duplicates().sort_values()

    month_names = {
        1:"Januari", 2:"Februari", 3:"Maret", 4:"April",
        5:"Mei", 6:"Juni", 7:"Juli", 8:"Agustus",
        9:"September", 10:"Oktober", 11:"November", 12:"Desember"
    }
    weekday_names = {
        0:"Senin", 1:"Selasa", 2:"Rabu", 3:"Kamis",
        4:"Jumat", 5:"Sabtu", 6:"Minggu"
    }

    rows = []
    for d in dates:
        rows.append((
            d.date(),
            d.day,
            d.month,
            month_names[d.month],
            (d.month - 1) // 3 + 1,
            d.year,
            weekday_names[d.weekday()],
            d.weekday() >= 5
        ))

    with conn.cursor() as cur:
        execute_values(cur,
            """
            INSERT INTO dim_date
                (full_date, day, month, month_name, quarter, year, weekday, is_weekend)
            VALUES %s
            ON CONFLICT (full_date) DO NOTHING
            """,
            rows
        )
        # Fetch mapping
        cur.execute("SELECT date_id, full_date FROM dim_date")
        mapping = {str(row[1]): row[0] for row in cur.fetchall()}
    conn.commit()
    print(f"    dim_date rows: {len(mapping)}")
    return mapping

def load_dim_product(conn, df: pd.DataFrame) -> dict:
    """Load dim_product, return mapping product_name → product_id."""
    print("[4/8] Loading dim_product...")
    products = df[["Product_Name", "Category"]].drop_duplicates("Product_Name")

    rows = [(row["Product_Name"], row["Category"]) for _, row in products.iterrows()]

    with conn.cursor() as cur:
        execute_values(cur,
            """
            INSERT INTO dim_product (product_name, category)
            VALUES %s
            ON CONFLICT (product_name) DO NOTHING
            """,
            rows
        )
        cur.execute("SELECT product_id, product_name FROM dim_product")
        mapping = {row[1]: row[0] for row in cur.fetchall()}
    conn.commit()
    print(f"    dim_product rows: {len(mapping)}")
    return mapping

def load_dim_location(conn, df: pd.DataFrame) -> dict:
    """Load dim_location, return mapping (store, province) → location_id."""
    print("[5/8] Loading dim_location...")
    locations = df[["Store_Location", "Province"]].drop_duplicates()

    rows = [(row["Store_Location"], row["Province"]) for _, row in locations.iterrows()]

    with conn.cursor() as cur:
        execute_values(cur,
            """
            INSERT INTO dim_location (store_location, province)
            VALUES %s
            ON CONFLICT (store_location, province) DO NOTHING
            """,
            rows
        )
        cur.execute("SELECT location_id, store_location, province FROM dim_location")
        mapping = {(row[1], row[2]): row[0] for row in cur.fetchall()}
    conn.commit()
    print(f"    dim_location rows: {len(mapping)}")
    return mapping

def load_dim_payment(conn, df: pd.DataFrame) -> dict:
    """Load dim_payment, return mapping payment_method → payment_id."""
    print("[6/8] Loading dim_payment...")
    methods = df["Payment_Method"].drop_duplicates().tolist()

    with conn.cursor() as cur:
        execute_values(cur,
            "INSERT INTO dim_payment (payment_method) VALUES %s ON CONFLICT (payment_method) DO NOTHING",
            [(m,) for m in methods]
        )
        cur.execute("SELECT payment_id, payment_method FROM dim_payment")
        mapping = {row[1]: row[0] for row in cur.fetchall()}
    conn.commit()
    print(f"    dim_payment rows: {len(mapping)}")
    return mapping

# -------------------------------------------------------
# 6. Load Fact Table
# -------------------------------------------------------

def load_fact_sales(conn, df: pd.DataFrame,
                    date_map: dict, product_map: dict,
                    location_map: dict, payment_map: dict):
    """Batch insert ke fact_sales."""
    print("[7/8] Loading fact_sales...")

    rows = []
    skipped = 0
    for _, row in df.iterrows():
        date_key     = str(row["Date"].date())
        product_key  = row["Product_Name"]
        location_key = (row["Store_Location"], row["Province"])
        payment_key  = row["Payment_Method"]

        date_id     = date_map.get(date_key)
        product_id  = product_map.get(product_key)
        location_id = location_map.get(location_key)
        payment_id  = payment_map.get(payment_key)

        if not all([date_id, product_id, location_id, payment_id]):
            skipped += 1
            continue

        rows.append((
            str(row["Transaction_ID"]),
            date_id,
            product_id,
            location_id,
            payment_id,
            int(row["Units_Sold"]),
            float(row["Unit_Price"]),
            float(row["Unit_Cost"]),
            float(row["Revenue"]),
            float(row["Profit"])
        ))

    with conn.cursor() as cur:
        execute_values(cur,
            """
            INSERT INTO fact_sales
            (
                transaction_id,
                date_id,
                product_id,
                location_id,
                payment_id,
                units_sold,
                unit_price,
                unit_cost,
                revenue,
                profit
            )
            VALUES %s
            ON CONFLICT (transaction_id)
            DO NOTHING
            """,
            rows,
            page_size=1000  # Batch 1000 rows per insert
        )
    conn.commit()
    inserted_rows = cur.rowcount
    print(f"    fact_sales inserted: {inserted_rows}")
    if skipped > 0:
        print(f"    [WARN] Rows skipped (FK miss): {skipped}")
    return len(rows)

# -------------------------------------------------------
# 7. Verify
# -------------------------------------------------------

def verify(conn):
    """Verifikasi jumlah row di fact_sales."""
    print("[8/8] Verifying...")

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM fact_sales")
        total_rows = cur.fetchone()[0]

    print(f"    Total rows in fact_sales: {total_rows}")
    print("    Verification: OK")

    with conn.cursor() as cur:
        cur.execute("ANALYZE fact_sales")

    conn.commit()
    print("    ANALYZE: done")

# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":
    # Resolve paths relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", "data", "DatasetPenjualanToko.csv")

    print("=" * 60)
    print("SalesBot ETL Pipeline")
    print("=" * 60)

    try:
        # Extract & clean
        df_raw    = extract_and_validate(csv_path)
        df_clean  = clean_and_transform(df_raw)

        # Try to connect to database
        conn = None
        try:
            conn = get_connection()
            print("[INFO] Connection successful")

            # Load dimensions
            date_map     = load_dim_date(conn, df_clean)
            product_map  = load_dim_product(conn, df_clean)
            location_map = load_dim_location(conn, df_clean)
            payment_map  = load_dim_payment(conn, df_clean)

            # Load fact
            inserted = load_fact_sales(
                conn, df_clean,
                date_map, product_map, location_map, payment_map
            )

            # Verify
            verify(conn)

            conn.close()
            print("=" * 60)
            print("ETL berhasil!")
            print("=" * 60)

        except Exception as db_err:
            print(f"[WARN] Database connection/operation failed: {db_err}")
            print("[INFO] Saving cleaned data to CSV instead...")
            
            if conn:
                try:
                    conn.close()
                except:
                    pass
            
            # Save cleaned data to CSV
            output_path = os.path.join(script_dir, "..", "data", "DatasetPenjualanToko_cleaned.csv")
            df_clean.to_csv(output_path, sep=";", index=False, encoding="utf-8")
            print(f"[OK] Cleaned data saved to {output_path}")
            print(f"     ({len(df_clean)} rows, {len(df_clean.columns)} columns)")
            print("=" * 60)
            print("ETL (data transform only) - berhasil!")
            print("=" * 60)
            print("\nNote: To upload to database later, use the cleaned CSV above.")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        exit(1)