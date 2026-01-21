from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todo as todos, Users
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    password: str = Field(min_length=6, max_length=16)
    newpassword: str = Field(min_length=6, max_length=16)


@router.get("/todo/me", status_code=status.HTTP_200_OK)
async def read_user_details(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=401, detail="Not authenticated to perform the request"
        )
    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.put("/todo/me/change-password", status_code=status.HTTP_200_OK)
async def change_user_password(
    db: db_dependency, user: user_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(
            status_code=401, detail="Not authenticated to perform the request"
        )
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user_model.hashed_password = bcrypt_context.hash(user_verification.newpassword)
    db.add(user_model)
    db.commit()
    return {"detail": "Password updated successfully"}
