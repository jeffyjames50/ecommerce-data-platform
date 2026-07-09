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


def load_dim_date():

    df = generate_date_dimension(
        "2020-01-01",
        "2030-12-31"
    )

    truncate_table("dim_date")

    load_dataframe(
        df,
        "dim_date"
    )


def generate_date_dimension(start_date, end_date):

    dates = pd.date_range(
        start=start_date,
        end=end_date
    )

    df = pd.DataFrame({
        "date_key": dates,
        "year": dates.year,
        "quarter": dates.quarter,
        "month": dates.month,
        "month_name": dates.month_name(),
        "week": dates.isocalendar().week,
        "day": dates.day,
        "day_name": dates.day_name()
    })

    return df


if __name__ == "__main__":
    load_dim_products()
    load_dim_date()