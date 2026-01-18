from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from models import Todo as todos

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
        
db_dependency = Annotated[Session, Depends(get_db)]                                                
        
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(todos).all()

@app.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id: int):
    todo_model =  db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found") 