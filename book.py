from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    rating: int

    def __init__(self, id, title, rating):
        self.id = id
        self.title = title
        self.rating = rating


Books = [
    Book(1, "Math", 4),
    Book(2, "Bangla", 2),
    Book(3, "English", 3),
]


@app.get("/readbook")
async def read_all():
    return Books


# Pydantic model implementation


class BookRequest(BaseModel):
    id: int = Field
    title: str = Field(min_length=1, max_length=100)  # Data Validation
    rating: int = Field(gt=0, lt=6)


@app.post("/create_book")
async def create_new_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(new_book)
    return {"message": "New Book appended successfully"}
