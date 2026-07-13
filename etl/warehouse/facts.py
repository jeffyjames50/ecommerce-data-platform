import pandas as pd

from etl.warehouse.loader import (
    read_staging_table,
    truncate_table,
    load_dataframe,
)

def transform_orders():

    orders = read_staging_table("orders")
    items = read_staging_table("order_items")

    df = orders.merge(
        items,
        on="order_id",
        how="inner"
    )

    df["total_amount"] = (
        df["quantity"] *
        df["unit_price"]
    )

    return df[
    [
        "order_item_id",
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "unit_price",
        "total_amount"
    ]
]


def load_fact_orders():

    df = transform_orders()

    truncate_table("fact_orders")

    load_dataframe(
        df,
        "fact_orders"
    )

def transform_user_events():

    df = read_staging_table("user_events")

    return df[
        [
            "event_id",
            "customer_id",
            "product_id",
            "event_type",
            "event_timestamp"
        ]
    ]


def load_fact_user_events():

    df = transform_user_events()

    truncate_table("fact_user_events")

    load_dataframe(
        df,
        "fact_user_events"
    )


if __name__ == "__main__":
    load_fact_orders()
    load_fact_user_events()