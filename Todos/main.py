from database import engine
import models
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from schemas import TodoRequest
from router import auth
from router import todos

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
