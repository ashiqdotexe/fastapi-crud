from fastapi import FastAPI

app = FastAPI()

Books = [
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
    {"title": "Title Three", "Author": "Author One", "Subject": "Math"},
    {"title": "Title Four", "Author": "Author One", "Subject": "Math"},
]


@app.get("/books")
async def read_books():
    return Books


# Dynamic Path Parameter
@app.get("/books/{particular_book}")
async def read_book(particular_book: str):
    for book in Books:
        if book.get("title").casefold() == particular_book.casefold():
            return book
