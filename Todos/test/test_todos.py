from ..router.todos import get_db, get_current_user, Todos
from starlette import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_readall_authenticate(test_todo):
    response = client.get("/todos")
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
    response = client.get("/todos/todo/1")
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
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_authenticated(test_todo):
    request_data = {
        "title": "cry now please",
        "description": "good for health",
        "priority": 2,
        "completed": False,
    }

    response = client.post("/todos/todo/", json=request_data)
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
    response = client.put("/todos/todo/1", json=request_data)
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
    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_one_authenticate(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestLocalSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
