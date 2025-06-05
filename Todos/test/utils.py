from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker, close_all_sessions
from ..database import Base
from Todos.main import app
from fastapi.testclient import TestClient
import pytest
from ..router.todos import get_db, get_current_user, Todos
from ..models import Users
from ..router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestLocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestLocalSession()
    try:
        yield db
    finally:
        close_all_sessions()


def override_get_current_user():
    return {"username": "sohan", "id": 1, "user_role": "admin"}


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Do homework",
        description="its important",
        priority=5,
        completed=False,
        owner_id=1,
    )
    db = TestLocalSession()
    db.add(todo)
    db.commit()
    yield todo
    with db.connection() as connect:
        connect.execute(text("DELETE FROM todos"))
        connect.commit()


@pytest.fixture
def test_user():
    user = Users(
        id=1,
        email="ashiqur",
        user_name="sohan",
        first_name="ashiqur",
        last_name="rohan",
        hashed_password=bcrypt_context.hash("aaaa"),
        is_active=False,
        role="admin",
        phone_number="01727",
    )
    db = TestLocalSession()
    db.add(user)
    db.commit()
    yield user
    with db.connection() as connect:
        connect.execute(text("DELETE FROM users"))
        connect.commit()


client = TestClient(app)
