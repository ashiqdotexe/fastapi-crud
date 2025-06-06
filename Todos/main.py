from .database import engine
from .models import Base
from fastapi import FastAPI, Request
from .router import auth, admin, todos, users
from fastapi.templating import Jinja2Templates


app = FastAPI()
Base.metadata.create_all(bind=engine)
template = Jinja2Templates(directory="Todos/templates")


@app.get("/")
def test(request: Request):
    return template.TemplateResponse("home.html", {"request": request})


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(todos.router)
