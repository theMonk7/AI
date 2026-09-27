"""Week 1 | Session 3 | File: structured_outputs.py
Topic: Schema-safe data validation with Pydantic.

Why this matters for AI engineering:
  - LLM outputs are strings. You cannot trust them to have the right shape.
  - Any AI pipeline that calls a model MUST validate the response before using it.
  - Pydantic is the standard for this validation in Python.

Concepts taught:
  1. BaseModel — define an expected schema
  2. Field constraints — enforce rules on individual fields
  3. ValidationError — what happens when data violates the schema
  4. Nested models — complex nested data structures
  5. model_dump / model_validate — convert between dict and model
  6. Simulated LLM output parsing — real-world usage pattern

Run:
    python src/weeks/week_01/llm_core/structured_outputs.py
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator


# ─────────────────────────────────────────────
# CONCEPT 1: BaseModel with Field constraints
# ─────────────────────────────────────────────
# BaseModel: declare the expected shape of your data.
# Field(): attach rules to individual fields.
#   - min_length / max_length: string length bounds
#   - ge / le: numeric greater-than-or-equal / less-than-or-equal
#   - pattern: regex constraint
class StudyTask(BaseModel):
    title: str = Field(min_length=5, max_length=80)
    difficulty: Literal["easy", "medium", "hard"]   # only these 3 values allowed
    estimated_minutes: int = Field(ge=10, le=240)
    outcome: str = Field(min_length=10)

    # ── SESSION 3 ASSIGNMENT ──────────────────────────────────────────────
    # field_validator runs AFTER the Field(ge=10, le=240) check passes.
    # It enforces custom business logic that Field() alone cannot express.
    # Rule: study blocks should be scheduled in 15-minute increments
    #       so they align with calendar slots (15, 30, 45, 60 … minutes).
    @field_validator("estimated_minutes")
    @classmethod
    def must_be_multiple_of_15(cls, v: int) -> int:
        if v % 15 != 0:
            raise ValueError(
                f"estimated_minutes must be a multiple of 15, got {v}. "
                f"Nearest valid values: {(v // 15) * 15} or {(v // 15 + 1) * 15}."
            )
        return v


# ─────────────────────────────────────────────
# CONCEPT 2: Nested models
# ─────────────────────────────────────────────
# Models can contain other models.
# This is how you define rich, structured LLM response schemas.
class Tag(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    category: Literal["skill", "tool", "concept"]


class WeeklyPlan(BaseModel):
    week_number: int = Field(ge=1, le=24)
    theme: str = Field(min_length=5)
    tasks: list[StudyTask]     # list of nested StudyTask objects
    tags: list[Tag]


# ─────────────────────────────────────────────
# CONCEPT 3: field_validator — custom logic
# ─────────────────────────────────────────────
# Sometimes Field() constraints are not enough.
# field_validator lets you write any Python validation logic.
class AgentResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: list[str]

    @field_validator("sources")
    @classmethod
    def sources_must_not_be_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("AgentResponse must include at least one source")
        return v

    @field_validator("answer")
    @classmethod
    def answer_must_not_be_vague(cls, v: str) -> str:
        vague = ["i don't know", "unclear", "n/a"]
        if v.strip().lower() in vague:
            raise ValueError(f"Answer '{v}' is too vague to be useful")
        return v


def parse_task(raw: dict) -> StudyTask:
    return StudyTask.model_validate(raw)


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────
def main() -> None:
    print("─── 1. Valid StudyTask ───")
    valid_task = {
        "title": "Build async retry client",
        "difficulty": "medium",
        "estimated_minutes": 90,
        "outcome": "Understand retry plus timeout behavior in async pipelines.",
    }
    task = parse_task(valid_task)
    print(task.model_dump())

    print()
    print("─── 2. Invalid StudyTask — multiple field violations ───")
    invalid_task = {
        "title": "X",           # too short (min 5)
        "difficulty": "expert", # not in Literal
        "estimated_minutes": 5, # below ge=10
        "outcome": "short",     # too short (min 10)
    }
    try:
        parse_task(invalid_task)
    except ValidationError as err:
        # Each error tells you: field, reason, input value
        for e in err.errors():
            print(f"  field={e['loc']} | type={e['type']} | input={e['input']!r}")

    print()
    print("─── 3. Nested WeeklyPlan ───")
    plan_data = {
        "week_number": 1,
        "theme": "Async Python and reliability foundations",
        "tasks": [
            {"title": "Study asyncio gather", "difficulty": "easy",
             "estimated_minutes": 60, "outcome": "Can run multiple coroutines concurrently."},
            {"title": "Build retry wrapper", "difficulty": "medium",
             "estimated_minutes": 90, "outcome": "Can handle transient API failures cleanly."},
        ],
        "tags": [
            {"name": "asyncio", "category": "tool"},
            {"name": "tenacity", "category": "tool"},
            {"name": "reliability", "category": "concept"},
        ],
    }
    plan = WeeklyPlan.model_validate(plan_data)
    print(f"Week {plan.week_number}: {plan.theme}")
    print(f"  Tasks: {[t.title for t in plan.tasks]}")
    print(f"  Tags:  {[t.name for t in plan.tags]}")

    print()
    print("─── 4. AgentResponse with custom validator ───")

    # Valid
    valid_response = AgentResponse(
        answer="Async reduces elapsed time by overlapping I/O waits.",
        confidence=0.92,
        sources=["asyncio docs", "python.org"],
    )
    print("Valid agent response:", valid_response.model_dump())

    # Invalid — no sources
    try:
        AgentResponse(answer="Some answer.", confidence=0.5, sources=[])
    except ValidationError as err:
        print("Caught:", err.errors()[0]["msg"])

    # Invalid — vague answer
    try:
        AgentResponse(answer="I don't know", confidence=0.1, sources=["wikipedia"])
    except ValidationError as err:
        print("Caught:", err.errors()[0]["msg"])

    print()
    print("─── 5. model_dump and model_validate round-trip ───")
    # model_dump() → dict  (use to serialize to JSON/DB)
    # model_validate() → model  (use to deserialize from JSON/API)
    as_dict = task.model_dump()
    restored = StudyTask.model_validate(as_dict)
    print("Round-trip successful:", task == restored)


if __name__ == "__main__":
    main()
