from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from sqlalchemy.orm import Session
from router.auth import get_current_user
from starlette import status
from models import Todos

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed"
        )
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed"
        )
    todos_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todos_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such id")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
