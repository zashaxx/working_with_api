from fastapi import FastAPI, Query, Body
from pydantic import BaseModel

app = FastAPI()


class Movie():
    def __init__(self, id, title, director, rating, description):
        self.id = id
        self.title = title
        self.director = director
        self.rating = rating
        self.description = description


MOVIES = [
    Movie(
        1,
        "Inception",
        "Christopher Nolan",
        9,
        "A mind-bending thriller about dreams within dreams.",
    ),
    Movie(
        2,
        "The Godfather",
        "Francis Ford Coppola",
        10,
        "An epic tale of a mafia family and their rise to power.",
    ),
    Movie(
        3,
        "Pulp Fiction",
        "Quentin Tarantino",
        9,
        "A darkly comedic crime film with intertwining stories.",
    ),
    Movie(
        4,
        "The Shawshank Redemption",
        "Frank Darabont",
        10,
        "A story of hope and friendship set in a prison.",
    ),
    Movie(
        5,
        "The Dark Knight",
        "Christopher Nolan",
        9,
        "A superhero film that explores the nature of chaos and order.",
    ),
    Movie(
        6,
        "Forrest Gump",
        "Robert Zemeckis",
        8,
        "The life journey of a simple man with a big heart.",
    ),
]


@app.get("/movies/")
async def get_movies():
    return MOVIES

@app.post("/create_movie")
async def create_movie(movie_request = Body()):
    MOVIES.append(movie_request)
