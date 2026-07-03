CREATE TABLE staging.customers (
    LIKE raw.customers INCLUDING ALL
);

CREATE TABLE staging.products (
    LIKE raw.products INCLUDING ALL
);

CREATE TABLE staging.orders (
    LIKE raw.orders INCLUDING ALL
);

CREATE TABLE staging.order_items (
    LIKE raw.order_items INCLUDING ALL
);

CREATE TABLE staging.user_events (
    LIKE raw.user_events INCLUDING ALL
);