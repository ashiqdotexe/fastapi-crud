from fastapi import FastAPI

app = FastAPI()

Books = [
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
    {"title": "Title One", "Author": "Author One", "Subject": "Math"},
]


@app.get("/books")
async def read_books():
    return Books
