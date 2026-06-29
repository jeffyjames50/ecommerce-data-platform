import pandas as pd
from sqlalchemy import create_engine
from config.database import DB_CONFIG


def get_engine():
    connection_string = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@{DB_CONFIG['host']}:"
        f"{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(connection_string)


def load_csv_to_postgres(csv_path, table_name, schema="raw"):
    engine = get_engine()

    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"⚠️ Skipping {table_name} (empty file)")
        return

    print(f"Loading {len(df)} rows into {schema}.{table_name}...")

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )

    print(f"✅ Loaded {table_name}")


def run_full_pipeline():
    base_path = "data/raw"

    tables = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "user_events": "user_events.csv"
    }

    for table_name, file_name in tables.items():
        csv_path = f"{base_path}/{file_name}"
        load_csv_to_postgres(csv_path, table_name)


if __name__ == "__main__":
    run_full_pipeline()