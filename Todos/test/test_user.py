from .utils import *
from ..router.users import get_current_user, get_db

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_user_authentication(test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "ashiqur",
        "user_name": "sohan",
        "first_name": "ashiqur",
        "last_name": "rohan",
        "hashed_password": "aaaa",
        "is_active": False,
        "role": "admin",
        "phone_number": "01727",
    }
