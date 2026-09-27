"""Sample Prefect flow for AI workflow orchestration learning."""

from __future__ import annotations

from prefect import flow, task


@task(retries=2, retry_delay_seconds=2)
def extract() -> dict:
    return {"message": "hello from prefect"}


@task
def transform(payload: dict) -> dict:
    return {"normalized_message": payload["message"].strip().lower()}


@task(retries=2, retry_delay_seconds=1)
def call_agent(payload: dict) -> dict:
    return {"ok": True, "agent_reply": f"processed:{payload['normalized_message']}"}


@task
def store_result(result: dict) -> None:
    print("Stored result:", result)


@flow(name="sample-agent-pipeline")
def run_pipeline() -> None:
    data = extract()
    normalized = transform(data)
    result = call_agent(normalized)
    store_result(result)


if __name__ == "__main__":
    run_pipeline()
