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