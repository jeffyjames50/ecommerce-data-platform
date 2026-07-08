import pandas as pd

from sqlalchemy import text

from etl.load_to_postgres import get_engine
from etl.logger import logger

def read_staging_table(table_name):
    engine = get_engine()

    query = f"""
        SELECT *
        FROM staging.{table_name}
    """

    return pd.read_sql(query, engine)


def truncate_table(table_name):
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(
            text(
                f"TRUNCATE TABLE warehouse.{table_name} CASCADE"
            )
        )
    logger.info(
        f"Truncated warehouse.{table_name}"
    )


def load_dataframe(df, table_name):
    engine = get_engine()

    df.to_sql(
        table_name,
        engine,
        schema="warehouse",
        if_exists="append",
        index=False
    )

    logger.info(
        f"Loaded {len(df)} rows into warehouse.{table_name}"
    )


