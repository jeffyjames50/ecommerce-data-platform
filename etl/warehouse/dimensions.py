import pandas as pd

from etl.warehouse.loader import (
    read_staging_table,
    truncate_table,
    load_dataframe,
)

def load_dim_products():

    df = read_staging_table("products")

    df = transform_products(df)

    truncate_table("dim_products")

    load_dataframe(df, "dim_products")


def transform_products(df):

    df = df.copy()

    df = df.rename(
        columns={
            "unit_price": "price"
        }
    )

    return df[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "price"
        ]
    ]


if __name__ == "__main__":
    load_dim_products()