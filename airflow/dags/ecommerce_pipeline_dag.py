from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def load_raw():
    from etl.load_to_postgres import run_full_pipeline
    run_full_pipeline(mode="refresh")


def load_staging():
    from etl.load_to_staging import run_staging_pipeline
    run_staging_pipeline()


def load_dimensions():
    from etl.warehouse.dimensions import (
        load_dim_customers,
        load_dim_products,
        load_dim_date,
    )

    load_dim_customers()
    load_dim_products()
    load_dim_date()


def load_facts():
    from etl.warehouse.facts import (
        load_fact_orders,
        load_fact_user_events,
    )

    load_fact_orders()
    load_fact_user_events()


default_args = {
    "owner": "data_engineering",
    "retries": 1,
}


with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:


    raw_task = PythonOperator(
        task_id="load_raw",
        python_callable=load_raw,
    )


    staging_task = PythonOperator(
        task_id="load_staging",
        python_callable=load_staging,
    )


    dimension_task = PythonOperator(
        task_id="load_dimensions",
        python_callable=load_dimensions,
    )


    fact_task = PythonOperator(
        task_id="load_facts",
        python_callable=load_facts,
    )


    raw_task >> staging_task >> dimension_task >> fact_task