from fastapi import HTTPException
from ..router.auth import (
    create_access_token,
    get_db,
    SECRET_KEY,
    ALGORITHM,
    authenticate_user,
)
from .utils import *
from starlette import status
from jose import jwt
from datetime import timedelta
import pytest_asyncio

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


def test_create_access_token():
    username = "sohan"
    id = 1
    role = "admin"

    token = create_access_token(username, id, role, timedelta(days=1))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == username
    assert payload["id"] == id
    assert payload["user_role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "sohan", "id": 1, "user_role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "sohan", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"user_role": "role"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excep:
        await get_current_user(token=token)
    assert excep.value.status_code == 401
    assert excep.value.detail == "Could not validate"
