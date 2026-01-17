from fastapi import FastAPI, Query ,Body
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {
        "title": "Silent Patient",
        "author": "Alex Michaelides",
        "year": 2001,
        "category": "science fiction",
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "category": "classic",
    },
    {"title": "1984", "author": "George Orwell", "year": 1949, "category": "classic"},
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "category": "classic",
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "category": "science fiction",
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "year": 1951,
        "category": "science fiction",
    },
    {"title": "title1", "author": "author1", "year": 2001, "category": "romance"},
]


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/my_book")
async def get_my_book():
    return {
        "title": "East of Eden",
        "author": "John Steinbeck",
        "year": 1952,
        "category": "category7",
    }


@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_new_book(new_book = Body()):
    BOOKS.append(new_book)
    