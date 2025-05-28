from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from schemas import UserRequest
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: UserRequest, db: db_dependency):
    new_user = Users(
        email=create_user_req.email,
        user_name=create_user_req.user_name,
        first_name=create_user_req.first_name,
        last_name=create_user_req.last_name,
        hashed_password=bcrypt_context.hash(create_user_req.password),
        is_active=True,
        role=create_user_req.role,
    )
    db.add(new_user)
    db.commit()
