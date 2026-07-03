import pandas as pd

from sqlalchemy import text

from etl.load_to_postgres import get_engine
from etl.logger import logger

def read_raw_table(table_name, engine):
    query = f"SELECT * FROM raw.{table_name}"
    return pd.read_sql(query, engine)

def truncate_staging_table(table_name, engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                f"TRUNCATE TABLE staging.{table_name} RESTART IDENTITY CASCADE"
            )
        )


def load_to_staging(df, table_name, engine):
    df.to_sql(
        table_name,
        engine,
        schema="staging",
        if_exists="append",
        index=False
    )

    logger.info(f"Loaded staging.{table_name}")


def transform_dataframe(df, table_name):
    if table_name == "customers":
        return transform_customers(df)

    elif table_name == "products":
        return transform_products(df)

    elif table_name == "orders":
        return transform_orders(df)

    elif table_name == "order_items":
        return transform_order_items(df)

    elif table_name == "user_events":
        return transform_user_events(df)

    return df


#customer transformation function
def transform_customers(df):
    df = df.copy()

    # Names → Title Case
    df["first_name"] = df["first_name"].str.strip().str.title()
    df["last_name"] = df["last_name"].str.strip().str.title()

    # Email → lowercase
    df["email"] = df["email"].str.strip().str.lower()

    # Country → standard format
    df["country"] = df["country"].str.strip().str.title()

    return df
#produc ttransformation function
def transform_products(df):
    df = df.copy()

    df["product_name"] = df["product_name"].str.strip()

    if "category" in df.columns:
        df["category"] = df["category"].str.strip().str.title()

    return df

#order transformation function
def transform_orders(df):
    df = df.copy()

    # Standardize order status
    if "status" in df.columns:
        df["status"] = df["status"].str.strip().str.lower()

    # Convert date if exists
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    return df

#order items transformation
def transform_order_items(df):
    df = df.copy()

    # Ensure numeric types
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    return df

#user events transformation
def transform_user_events(df):
    df = df.copy()

    if "event_type" in df.columns:
        df["event_type"] = df["event_type"].str.strip().str.lower()

    if "event_time" in df.columns:
        df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

    return df

def process_table(table_name, engine):
    logger.info(f"Processing staging table: {table_name}")

    df = read_raw_table(table_name, engine)

    df = transform_dataframe(df, table_name)

    truncate_staging_table(table_name, engine)

    load_to_staging(df, table_name, engine)

#pipeline runner
def run_staging_pipeline():
    engine = get_engine()

    tables = [
        "customers",
        "products",
        "orders",
        "order_items",
        "user_events"
    ]

    for table in tables:
        process_table(table, engine)

    logger.info("Staging pipeline completed successfully.")



if __name__ == "__main__":
    run_staging_pipeline()