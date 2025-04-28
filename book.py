from fastapi import FastAPI

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
    Book(1, "Math", "4"),
    Book(2, "Bangla", "2"),
    Book(3, "English", "3"),
]


@app.get("/readbook")
async def read_all():
    return Books
