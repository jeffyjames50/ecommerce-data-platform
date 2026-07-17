from etl.load_to_postgres import get_engine
from sqlalchemy import text


def validate_table_count(table_name, expected_min=1):
    engine = get_engine()

    query = f"""
        SELECT COUNT(*)
        FROM warehouse.{table_name}
    """

    with engine.connect() as conn:
        count = conn.execute(text(query)).scalar()

    if count < expected_min:
        raise Exception(
            f"{table_name} validation failed. Count={count}"
        )

    print(f"{table_name}: {count} rows OK")


def run_validation():
    validate_table_count("dim_customers")
    validate_table_count("dim_products")
    validate_table_count("fact_orders")
    validate_table_count("fact_user_events")

    print("Warehouse validation successful")


if __name__ == "__main__":
    run_validation()