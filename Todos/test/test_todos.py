from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker, close_all_sessions
from ..database import Base
from ..main import app
from ..router.todos import get_db, get_current_user, Todos
from fastapi.testclient import TestClient
from starlette import status
import pytest

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


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)


def test_readall_authenticate(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Do homework",
            "description": "its important",
            "priority": 5,
            "completed": False,
            "owner_id": 1,
            "id": 1,
        }
    ]


def test_read_one_authenticate(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "Do homework",
        "description": "its important",
        "priority": 5,
        "completed": False,
        "owner_id": 1,
        "id": 1,
    }


def test_read_one_not_authenticate(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_authenticated(test_todo):
    request_data = {
        "title": "cry now please",
        "description": "good for health",
        "priority": 2,
        "completed": False,
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestLocalSession()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == "cry now please"
    assert model.description == "good for health"
    assert model.priority == 2
    assert model.completed == False


def test_update_one_authenticate(test_todo):
    request_data = {
        "title": "laugh now please",
        "description": "good for health",
        "priority": 2,
        "completed": False,
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestLocalSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "laugh now please"


def test_update_one_not_authenticate(test_todo):
    request_data = {
        "title": "laugh now please",
        "description": "good for health",
        "priority": 2,
        "completed": False,
    }
    response = client.put("/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_one_authenticate(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestLocalSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
