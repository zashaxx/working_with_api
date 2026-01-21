from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todo as todos
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=401, detail="you need admin privileges to perform this request"
        )
    return db.query(todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(ge=1)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=401, detail="you need admin privileges to perform this request"
        )
    todo_model = db.query(todos).filter(todos.id == todo_id).delete()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.commit()
    return {"detail": "Todo deleted successfully"}
