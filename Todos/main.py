from .database import engine
from .models import Base
from fastapi import FastAPI, Request
from .router import auth, admin, todos, users
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

app = FastAPI()
Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="Todos/static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(todos.router)
