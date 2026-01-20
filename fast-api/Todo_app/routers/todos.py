from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field 
from database import SessionLocal
from models import Todo as todos


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title : str = Field (min_length = 1, max_length =50)
    description: str = Field(min_length =1, max_length = 250)
    priority: int = Field(ge=1, le=5)
    completed : bool
                                        
    
@router.get("/")
async def read_all(db: db_dependency):
    return db.query(todos).all()

@router.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id: int = Path (ge=1)):
    todo_model =  db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found") 

@router.post("/todo/add-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, Todo_Request: TodoRequest):
    todo_model = todos(**Todo_Request.model_dump())
    db.add(todo_model)
    db.commit()
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_request: TodoRequest, todo_id:int = Path(ge=1)):
    todo_model = db.query(todos).filter(todos.id == todo_id ).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail ="Todo not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed
    
    db.add(todo_model)
    db.commit()

@router.delete("/todos/{todo_id}", status_code =status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int = Path(ge =1 )):
    todo_model = db.query(todos).filter(todos.id == todo_id).delete()
    if todo_model is None:
        raise HTTPException (status_code = 404 , detail = "Todo not found")
    db.commit()
    