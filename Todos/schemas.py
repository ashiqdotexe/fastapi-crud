from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    email: str
    user_name: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str


class UserPass(BaseModel):
    current_pass: str
    new_pass: str
    confirm_pass: str


class TodoRequest(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=2)
    priority: int = Field(gt=0, lt=6)
    completed: bool = Field(default=False)


class Token(BaseModel):
    access_token: str
    token_type: str
