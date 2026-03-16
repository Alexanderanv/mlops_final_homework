from datetime import datetime
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(str(Path(__file__).resolve().parent))
import runner

dag = DAG(
    "first",
    schedule="33 4 * * *",
    start_date=datetime.fromisoformat("2026-03-16T15:10:00Z"),
)

extract_data = PythonOperator(
    task_id="extract_data",
    python_callable=runner.extract_data,
    dag=dag,
)

extract_from_clickhouse = PythonOperator(
    task_id="extract_from_clickhouse",
    python_callable=runner.extract_from_clickhouse,
    dag=dag,
)
train = PythonOperator(
    task_id="train",
    python_callable=runner.train,
    dag=dag,
)

[extract_data, extract_from_clickhouse] >> train