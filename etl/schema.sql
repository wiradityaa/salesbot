-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE        NOT NULL UNIQUE,
    day         INT         NOT NULL,
    month       INT         NOT NULL,
    month_name  VARCHAR(20) NOT NULL,
    quarter     INT         NOT NULL,
    year        INT         NOT NULL,
    weekday     VARCHAR(10) NOT NULL,
    is_weekend  BOOLEAN     NOT NULL
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    product_id   SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    category     VARCHAR(50)  NOT NULL
);

-- Dimension: Location
CREATE TABLE IF NOT EXISTS dim_location (
    location_id    SERIAL PRIMARY KEY,
    store_location VARCHAR(100) NOT NULL,
    province       VARCHAR(50)  NOT NULL,
    UNIQUE(store_location, province)
);

-- Dimension: Payment
CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id     SERIAL PRIMARY KEY,
    payment_method VARCHAR(50) NOT NULL UNIQUE
);

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id   SERIAL          PRIMARY KEY,
    date_id    INT             NOT NULL REFERENCES dim_date(date_id),
    product_id INT             NOT NULL REFERENCES dim_product(product_id),
    location_id INT            NOT NULL REFERENCES dim_location(location_id),
    payment_id INT             NOT NULL REFERENCES dim_payment(payment_id),
    units_sold INT             NOT NULL,
    unit_price DECIMAL(10,2)   NOT NULL,
    unit_cost  DECIMAL(10,2)   NOT NULL,
    revenue    DECIMAL(14,2)   NOT NULL,
    profit     DECIMAL(14,2)   NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_sales_date     ON fact_sales(date_id);
CREATE INDEX IF NOT EXISTS idx_sales_product  ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_location ON fact_sales(location_id);
CREATE INDEX IF NOT EXISTS idx_sales_payment  ON fact_sales(payment_id);
CREATE INDEX IF NOT EXISTS idx_date_ym        ON dim_date(year, month);
CREATE INDEX IF NOT EXISTS idx_loc_province   ON dim_location(province);