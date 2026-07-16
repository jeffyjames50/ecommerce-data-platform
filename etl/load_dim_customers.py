import pandas as pd
from sqlalchemy import text

from etl.load_to_postgres import get_engine
from etl.logger import logger

def extract_customers(engine):
    query = "SELECT * FROM staging.customers"
    return pd.read_sql(query, engine)

def transform_customers(df):
    return df[[
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country"
    ]]


def load_dim_customers(df, engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                "TRUNCATE TABLE warehouse.dim_customers CASCADE"
            )
        )

    df.to_sql(
        "dim_customers",
        engine,
        schema="warehouse",
        if_exists="append",
        index=False
    )

    logger.info("Loaded warehouse.dim_customers")


def run():
    engine = get_engine()

    df = extract_customers(engine)
    df = transform_customers(df)
    load_dim_customers(df, engine)


if __name__ == "__main__":
    run()

