from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas import TodoRequest


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="No such todo id")


# Create new ToDo list-->
@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_req: TodoRequest):
    new_todo = Todos(**todo_req.model_dump())
    db.add(new_todo)
    db.commit()


# Update todo
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_req: TodoRequest, todo_id: int = Path(gt=0)
):
    new_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if new_todo is None:
        raise HTTPException(status_code=404, detail="No such Todo")
    new_todo.title = todo_req.title
    new_todo.description = todo_req.description
    new_todo.priority = todo_req.priority
    new_todo.completed = todo_req.completed
    db.add(new_todo)
    db.commit()


# Delete todo
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    new_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if new_todo is None:
        raise HTTPException(status_code=404, detail="no such todo")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
