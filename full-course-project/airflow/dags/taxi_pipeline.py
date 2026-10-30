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
DBT = f"{PROJECT}/.venv-data-engineering/bin/dbt"
MONTHS = "2024-01 2024-02"

with DAG(
    dag_id="taxi_pipeline",
    schedule="@monthly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
):
    download = BashOperator(task_id="download", bash_command=f"{PY} taxi/download.py {MONTHS}", cwd=str(PROJECT))
    ingest = BashOperator(task_id="ingest", bash_command=f"{PY} taxi/ingest.py {MONTHS}", cwd=str(PROJECT))
    dbt_build = BashOperator(task_id="dbt_build", bash_command=f"{DBT} build", cwd=str(PROJECT / "taxi" / "taxi_dbt"))
    report = BashOperator(task_id="report", bash_command=f"{PY} taxi/report.py", cwd=str(PROJECT))

    download >> ingest >> dbt_build >> report