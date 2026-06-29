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


def load_table(csv_path, table_name, schema="raw"):
    engine = get_engine()

    df = pd.read_csv(csv_path)

    print(f"Loading {len(df)} rows into {schema}.{table_name}...")

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )

    print(f"Successfully loaded {table_name}")


if __name__ == "__main__":
    load_table(
        "data/raw/customers.csv",
        "customers"
    )