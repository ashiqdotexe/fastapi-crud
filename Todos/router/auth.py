from fastapi import APIRouter
from starlette import status
from schemas import UserRequest
from models import Users

router = APIRouter()


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: UserRequest):
    new_user = Users(
        email=create_user_req.email,
        user_name=create_user_req.user_name,
        first_name=create_user_req.first_name,
        last_name=create_user_req.last_name,
        hashed_password=create_user_req.password,
        is_active=True,
        role=create_user_req.role,
    )
    if new_user:
        return new_user
