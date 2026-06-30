REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "city",
        "signup_date",
    ],
    "products": [
        "product_id",
        "product_name",
        "category",
        "brand",
        "unit_price",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
        "total_amount",
    ],
    "order_items": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
    ],
    "user_events": [
        "event_id",
        "customer_id",
        "product_id",
        "event_type",
        "event_timestamp",
    ],
}

PRIMARY_KEYS = {
    "customers": ["customer_id"],
    "products": ["product_id"],
    "orders": ["order_id"],
    "order_items": ["order_item_id"],
    "user_events": ["event_id"],
}

REQUIRED_NOT_NULL = {
    "customers": ["customer_id", "email"],
    "products": ["product_id", "unit_price"],
    "orders": ["order_id", "customer_id"],
    "order_items": ["order_item_id", "order_id", "product_id"],
    "user_events": ["event_id", "customer_id"],
}

POSITIVE_NUMERIC_COLUMNS = {
    "products": ["unit_price"],
    "orders": ["total_amount"],
    "order_items": ["quantity", "unit_price"],
}