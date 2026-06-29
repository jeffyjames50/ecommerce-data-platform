CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    country VARCHAR(100),
    city VARCHAR(100),
    signup_date DATE
);


CREATE TABLE IF NOT EXISTS raw.products (
    product_id INTEGER,
    product_name VARCHAR(255),
    category VARCHAR(100),
    brand VARCHAR(255),
    unit_price DECIMAL(10,2)
);


CREATE TABLE IF NOT EXISTS raw.orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    order_status VARCHAR(50),
    total_amount DECIMAL(10,2)
);



CREATE TABLE IF NOT EXISTS raw.order_items (
    order_item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2)
);



CREATE TABLE IF NOT EXISTS raw.user_events (
    event_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP
);