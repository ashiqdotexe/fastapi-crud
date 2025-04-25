from fastapi import FastAPI, Body

app = FastAPI()

Books = [
    {"title": "Title One", "Author": "Author One", "Subject": "Science"},
    {"title": "Title One", "Author": "Author Two", "Subject": "History"},
    {"title": "Title Three", "Author": "Author Two", "Subject": "Math"},
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


# Query Parameter-->
@app.get("/books/")
async def read_books_by_query(subject: str):
    return_all_book = []
    for book in Books:
        if book.get("Subject").casefold() == subject.casefold():
            return_all_book.append(book)
    return return_all_book


# Assignment -->>
@app.get("/books/get_author/")
async def get_author(author: str):
    authors = []
    for book in Books:
        if book.get("Author").casefold() == author.casefold():
            authors.append(book)
    return authors


# Query Parameter with path parameter
@app.get("/books/{book_author}/")
async def read_books_by_query_path(book_author: str, subject: str):
    return_all_book = []
    for book in Books:
        if (
            book.get("Author").casefold() == book_author.casefold()
            and book.get("Subject").casefold() == subject.casefold()
        ):
            return_all_book.append(book)
    return return_all_book


##Post method-->
@app.post("/create_books")
async def create_book(new_book=Body()):
    Books.append(new_book)


# Put (Update) method-->
@app.put("/books/update_books")
async def update_book(up_book=Body()):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == up_book.get("title").casefold():
            Books[i] = up_book


# delete method
@app.delete("/books/delete_books/{delete_book}/")
async def delete_books(delete_book: str):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == delete_book.casefold():
            Books.pop(i)
            break
