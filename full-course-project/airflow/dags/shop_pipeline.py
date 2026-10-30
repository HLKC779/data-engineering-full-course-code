from datetime import datetime, timedelta
from pathlib import Path

try:
    from airflow.sdk import DAG
except ImportError:  # Airflow 2.x
    from airflow import DAG

try:
    from airflow.providers.standard.operators.bash import BashOperator
except ImportError:  # Airflow 2.x fallback
    from airflow.operators.bash import BashOperator

PROJECT = Path(__file__).resolve().parents[2]
PY = f"{PROJECT}/.venv-data-engineering/bin/python"

with DAG(
    dag_id="shop_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(seconds=30)},
):
    test_code = BashOperator(task_id="test_code", bash_command=f"{PY} -m pytest -q tests", cwd=str(PROJECT))
    load_raw = BashOperator(task_id="load_raw", bash_command="sqlite3 shop.db < sql/load_shop.sql", cwd=str(PROJECT))
    dedupe = BashOperator(task_id="dedupe", bash_command="sqlite3 shop.db < sql/dedupe.sql", cwd=str(PROJECT))
    transform = BashOperator(task_id="transform", bash_command=f"{PY} etl_pandas.py", cwd=str(PROJECT))

    test_code >> load_raw >> dedupe >> transform