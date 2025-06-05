from .utils import *
from ..router.users import get_current_user, get_db
from ..router.auth import bcrypt_context

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_user_authentication(test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "ashiqur"
    assert data["user_name"] == "sohan"
    assert data["first_name"] == "ashiqur"
    assert data["last_name"] == "rohan"
    assert data["role"] == "admin"
    assert data["phone_number"] == "01727"
    assert "hashed_password" in data  # optional
    assert data["id"] == 1


def test_user_password(test_user):
    response_data = {
        "current_pass": bcrypt_context.hash("aaaa"),
        "new_pass": bcrypt_context.hash("new_password"),
        "confirm_pass": bcrypt_context.hash("new_password"),
    }
    ressponse = client.put(
        "/users/changepassword",
        json={
            "current_pass": "aaaa",
            "new_pass": "new_password",
            "confirm_pass": "new_password",
        },
    )
    assert ressponse.status_code == 204
