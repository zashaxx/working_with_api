from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Movie: 
    def __init__(self, id, title, director, rating, description,publication_year):
        self.id = id
        self.title = title
        self.director = director
        self.rating = rating
        self.description = description
        self.publication_year = publication_year


class Movie_Request(BaseModel):
    id: Optional[int] = Field(description="ID is not required on create", default=None)
    title: str = Field(min_length=3)
    director: str = Field(min_length=3)
    rating: int = Field(gt=-1, lt=11)
    description: str = Field(min_length=10, max_length=100)
    publication_year: int = Field(gt=1800, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Matrix",
                "director": "Wachowskis",
                "rating": 8,
                "description": "A sci-fi action movie",
                "publication_year": 1999,
            }
        }
    }


MOVIES = [
    Movie(
        1,
        "Inception",
        "Christopher Nolan",
        9,
        "A mind-bending thriller about dreams within dreams.",
        2010
    ),
    Movie(
        2,
        "The Godfather",
        "Francis Ford Coppola",
        10,
        "An epic tale of a mafia family and their rise to power.",
        1972
    ),
    Movie(
        3,
        "Pulp Fiction",
        "Quentin Tarantino",
        9,
        "A darkly comedic crime film with intertwining stories.",
        1994
    ),
    Movie(
        4,
        "The Shawshank Redemption",
        "Frank Darabont",
        10,
        "A story of hope and friendship set in a prison.",
        1994
    ),
    Movie(
        5,
        "The Dark Knight",
        "Christopher Nolan",
        9,
        "A superhero film that explores the nature of chaos and order.",
        2008
    ),
    Movie(
        6,
        "Forrest Gump",
        "Robert Zemeckis",
        8,
        "The life journey of a simple man with a big heart.",
        1994
    ),
]


@app.get("/movies/")
async def get_movies():
    return MOVIES

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    for movie in MOVIES:
        if movie.id == movie_id:
            return movie

@app.get("/books/")
async def read_movie_by_rating (movie_rating : int ):
    movies_to_return = []
    for movie in MOVIES :
        if movie.rating == movie_rating:
            movies_to_return.append(movie)
    return movies_to_return

@app.get("/movies/publication_year/{publication_year}")
async def read_movie_by_publication_year (publication_year :int):
    movies_to_return = []
    for movie in MOVIES :
        if movie.publication_year == publication_year:
            movies_to_return.append(movie)
    return movies_to_return


@app.post("/create_movie")
async def create_movie(movie_request: Movie_Request):
    new_movie = Movie(**movie_request.model_dump())
    MOVIES.append(find_movie_by_id(new_movie))
    return new_movie


def find_movie_by_id(movie: Movie):

    movie.id = 1 if len(MOVIES) == 0 else MOVIES[-1].id + 1

    # if len(MOVIES) > 0:
    #     movie.id = MOVIES[-1].id + 1
    # else:
    #     movie.id = 1

    return movie


@app.put("/movies/update_movie")
async def update_movie(movie_request: Movie_Request):
    for i in range (len(MOVIES)):
        if  MOVIES[i].id == movie_request.id:
            MOVIES[i] = movie_request

@app.delete("/movies/delete_movie/{movie_id}")
async def delete_movie(movie_id: int):
    for i in range (len(MOVIES)):
        if  MOVIES[i].id == movie_id:
            MOVIES.pop(i)
            return {"message":"movie deleted"}
    return {"message":"movie not found"}

