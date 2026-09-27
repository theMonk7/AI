from fastapi import APIRouter, Path
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class User(BaseModel):
    id: int
    username: str
    email: str

db = [User(id=i, username=f"username{i}", email=f"email{i}") for i in range(100)]

@router.get("/")
async def users():
    return db


@router.get("/users/{id}")
async def get_user(id: int = Path(..., ge=0)):
    user = filter(lambda u: u.id == id, db)
    for u in user:
        print(u)
        return u
    return "pikachu"

@router.post("/users")
async def create_user(user: User):
    db.append(user)
    return {"username": f"username{user.id}"}