from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from ..schemas import UserRequest, Token
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Authentication
def authenticate_user(user_name, password, db):
    user = db.query(Users).filter(Users.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


# Encoding jwt:
SECRET_KEY = "9b43e914a1317f1cfc96aab67bf49d334c33bbf4043830ca63c2a6021c3bb4b3"
ALGORITHM = "HS256"


def create_access_token(
    user_name: str, id: int, user_role: str, exp_datetime: timedelta
):
    encode = {"sub": user_name, "id": id, "user_role": user_role}
    expires = datetime.now(timezone.utc) + exp_datetime
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# decoding
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("user_role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate"
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate"
        )


# Endpoints
@router.post("/", status_code=status.HTTP_201_CREATED)
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
        phone_number=create_user_req.phone_number,
    )
    db.add(new_user)
    db.commit()


@router.post("/token", response_model=Token)
async def login_authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Authentication Failed"
    token = create_access_token(
        user.user_name, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
