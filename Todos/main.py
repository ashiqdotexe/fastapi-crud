from .database import engine
from .models import Base
from fastapi import FastAPI
from .router import auth, admin, todos, users

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def read_healthy():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(todos.router)
