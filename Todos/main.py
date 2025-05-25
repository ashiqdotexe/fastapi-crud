from database import engine
import models
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas import TodoRequest

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="No such todo id")


# Create new ToDo list-->
@app.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_req: TodoRequest):
    new_todo = Todos(**todo_req.model_dump())
    db.add(new_todo)
    db.commit()
