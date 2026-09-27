"""Sample Airflow DAG for AI workflow orchestration learning.

This DAG is intentionally minimal for Week 16 comparison exercises.
"""

from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract_task() -> None:
    print("Extract: receive webhook payload or scheduled trigger")


def transform_task() -> None:
    print("Transform: normalize input for agent service")


def call_agent_task() -> None:
    print("Call Agent: invoke Python/FastAPI endpoint")


def store_result_task() -> None:
    print("Store: persist result and emit audit log")


with DAG(
    dag_id="sample_agent_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning", "agentic-ai"],
) as dag:
    extract = PythonOperator(task_id="extract", python_callable=extract_task)
    transform = PythonOperator(task_id="transform", python_callable=transform_task)
    call_agent = PythonOperator(task_id="call_agent", python_callable=call_agent_task)
    store_result = PythonOperator(task_id="store_result", python_callable=store_result_task)

    extract >> transform >> call_agent >> store_result
