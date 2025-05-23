from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    rating: int
    published_date: int

    def __init__(self, id, title, rating, published_date):
        self.id = id
        self.title = title
        self.rating = rating
        self.published_date = published_date


Books = [
    Book(1, "Math", 4, 2012),
    Book(2, "Bangla", 4, 2016),
    Book(3, "English", 3, 2012),
]


@app.get("/readbook")
async def read_all():
    return Books


# Pydantic model implementation


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)  # Data Validation
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {"title": "A new book", "rating": 5, "published_date": 2000}
        }
    }


# Fetching book according to id
@app.get("/readbook/{book_id}")
async def read_book_id(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book


# Fetching book according to rating
@app.get("/readbook/")
async def read_book_by_id(book_rating: int):
    book_to_return = []
    for book in Books:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return


###Assignment----->>>


# Fetching by published_date
@app.get("/readbook/publish/")
async def read_by_publish(published_date: int):
    book_to_return = []
    for book in Books:
        if book.published_date == published_date:
            book_to_return.append(book)
    return book_to_return


##Book creation
@app.post("/create_book")
async def create_new_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))
    return {"message": "New Book appended successfully"}


# Adding book in chronological book_id
def find_book_id(book: Book):
    if len(Books) == 0:
        book.id = 1
    else:
        book.id = Books[-1].id + 1
    return book


# updating books using book_id
@app.put("/readbook/update_book")
async def update_book_by_id(book: BookRequest):
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
    return {"message": "Book updated successfully"}


# Delete book using book_id
@app.delete("/readbook/delete_book/{book_id}")
async def delete_book_by_id(book_id: int = Path(gt=0)):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break
    return {"message": "Book deleted successfully"}
