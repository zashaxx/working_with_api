from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Simple API", version="1.0")

class ItemIn(BaseModel):
    name: str  # name of books
    price: float  # price of books
    in_stock: bool  # availability of books

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

# In-memory storage for items
DB: dict[int, ItemIn] = {}
NEXT_ID = 1

@app.get("/")
def root():
    return {"message": "Welcome to the Simple API"}

@app.get("/items")
def list_items(
    q: str | None = Query(default=None, description="Search query for item names")
):
    if q is None:
        return DB
    
    # Filter items by search query
    return {id: item for id, item in DB.items() if q.lower() in item.name.lower()}