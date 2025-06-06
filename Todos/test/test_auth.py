from ..router.auth import (
    create_access_token,
    get_db,
    SECRET_KEY,
    ALGORITHM,
    authenticate_user,
)
from .utils import *
from starlette import status

app.dependency_overrides[get_db] = get_db


def test_authenticate_user_auth(test_user):
    db = TestLocalSession()

    authenticated_user = authenticate_user(test_user.user_name, "aaaa", db)
    assert authenticated_user is not None
    assert authenticated_user.user_name == test_user.user_name
    non_authenticated_user = authenticate_user("Wrong user name", "aaaa", db)
    assert non_authenticated_user is False
    non_authenticated_pass = authenticate_user(test_user.user_name, "adadada", db)
    assert non_authenticated_pass is False
