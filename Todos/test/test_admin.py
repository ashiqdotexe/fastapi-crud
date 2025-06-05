from .utils import *
from ..router.admin import get_current_user, get_db
from ..models import Todos
from starlette import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_admin(test_todo):
    response = client.get("/admin/todo/")
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


def test_delete_admin_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204
    db = TestLocalSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
