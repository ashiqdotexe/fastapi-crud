from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from schemas import UserRequest
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(user_name, password, db):
    user = db.query(Users).filter(Users.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_req: UserRequest,
    db: db_dependency,
):
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


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def login_authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Authentication Failed"
    return "Successful authentication"
