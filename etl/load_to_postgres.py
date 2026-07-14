import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

from config.database import DB_CONFIG
from config.settings import (
    REQUIRED_COLUMNS,
    PRIMARY_KEYS,
    REQUIRED_NOT_NULL,
    POSITIVE_NUMERIC_COLUMNS,
)

from etl.profiler import (
    DataProfiler,
    save_profile_report,
)

from etl.logger import logger
from etl.validator import DataValidator


def get_engine():
    connection_string = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:"
        f"{DB_CONFIG['port']}/"
        f"{DB_CONFIG['database']}"
    )
    return create_engine(connection_string)


def truncate_table(engine, schema, table_name):
    with engine.begin() as conn:
        conn.execute(
            text(
                f"TRUNCATE TABLE {schema}.{table_name} "
                "RESTART IDENTITY CASCADE"
            )
        )


def validate_dataset(df, table_name):
    DataValidator.check_empty(df)

    DataValidator.check_required_columns(
        df,
        REQUIRED_COLUMNS[table_name]
    )

    DataValidator.check_duplicates(
        df,
        PRIMARY_KEYS[table_name]
    )

    DataValidator.check_nulls(
        df,
        REQUIRED_NOT_NULL[table_name]
    )

    if table_name in POSITIVE_NUMERIC_COLUMNS:
        DataValidator.check_positive_values(
            df,
            POSITIVE_NUMERIC_COLUMNS[table_name]
        )



def load_dataframe(df, table_name, engine, schema="raw"):
    logger.info(f"Loading {len(df)} rows into {schema}.{table_name}")

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )

    logger.info(f"Successfully loaded {table_name}")


def load_csv_to_postgres(csv_path, table_name, engine, schema="raw", mode="refresh"):
    logger.info(f"Processing table: {table_name}")

    # 1. Validate file exists
    DataValidator.file_exists(csv_path)

    # 2. Read data (controlled way)
    df = DataValidator.read_csv(csv_path)

    # 3. Validation layer
    validate_dataset(df, table_name)

    profile = DataProfiler.profile_dataframe(df)

    report_path = save_profile_report(profile,table_name)

    logger.info(f"Profile report saved: {report_path}")

    # 4. Refresh logic
    if mode == "refresh":
        truncate_table(engine, schema, table_name)

    # 5. Load data
    load_dataframe(df, table_name, engine, schema)




def run_full_pipeline(mode="refresh"):
    BASE_DIR = Path(__file__).resolve().parents[1]
    base_path = BASE_DIR / "data" / "raw"
    engine = get_engine()

    tables = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "user_events": "user_events.csv"
    }

    for table_name, file_name in tables.items():
        csv_path = base_path / file_name

        load_csv_to_postgres(
            csv_path,
            table_name,
            engine,
            mode=mode
        )


if __name__ == "__main__":
    run_full_pipeline(mode="refresh")