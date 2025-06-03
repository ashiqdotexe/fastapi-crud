from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas import TodoRequest
from router.auth import get_current_user
from schemas import UserPass
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    user_model = db.query(Users).filter(Users.user_name == user.get("username")).first()
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
        )
    return user_model


@router.put("/todo", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, password_chng: UserPass
):
    new_user = db.query(Users).filter(Users.user_name == user.get("username")).first()
    if not new_user or new_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
        )
    if not bcrypt_context.verify(password_chng.current_pass, new_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
        )
    if password_chng.new_pass != password_chng.confirm_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please re confirm the password",
        )
    new_user.hashed_password = bcrypt_context.hash(password_chng.new_pass)
    db.add(new_user)
    db.commit()


@router.put("/phone/{phone number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorize for update phone number",
        )
    new_user = db.query(Users).filter(Users.id == user.get("id")).first()
    new_user.phone_number = phone_number
    db.add(new_user)
    db.commit()
