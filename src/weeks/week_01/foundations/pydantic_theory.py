from __future__ import annotations
from typing import Literal,List
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field


app = FastAPI(
    title="Agent Echo API",
    description="Week 1 teaching API — demonstrates FastAPI + Pydantic patterns",
    version="0.1.0",
)
class EchoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)

class EchoResponse(BaseModel):
    ok: bool
    agent_reply: str
    message_length: int

class TaskRequest(BaseModel):
    task: str = Field(min_length=5)
    priority: Literal["low", "medium", "high"] = "medium"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    priority: str
    message: str

class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    version: str

@app.get("/health/{id}", response_model=HealthResponse)
def health_check(id: int, user_id: int, health_id: int = Query(..., ge=4, lt=100)) -> HealthResponse:
    return HealthResponse(status="healthy", version=f"0.1.0::{health_id}:{user_id}")



class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []

@app.post("/students/")
async def student_data(s1: Student):
   return s1