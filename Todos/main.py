from database import engine
import models
from fastapi import FastAPI

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
