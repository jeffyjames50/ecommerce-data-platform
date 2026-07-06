CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    product_id INT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    brand TEXT,
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key DATE PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name TEXT NOT NULL,
    week INT NOT NULL,
    day INT NOT NULL,
    day_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_fact_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES warehouse.dim_customers(customer_id),

    CONSTRAINT fk_fact_orders_product
        FOREIGN KEY (product_id)
        REFERENCES warehouse.dim_products(product_id),

    CONSTRAINT fk_fact_orders_date
        FOREIGN KEY (order_date)
        REFERENCES warehouse.dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_user_events (
    event_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    event_type TEXT,
    event_timestamp TIMESTAMP,

    CONSTRAINT fk_events_customer
        FOREIGN KEY (customer_id)
        REFERENCES warehouse.dim_customers(customer_id),

    CONSTRAINT fk_events_product
        FOREIGN KEY (product_id)
        REFERENCES warehouse.dim_products(product_id)
);


