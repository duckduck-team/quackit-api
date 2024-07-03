from pydantic import BaseModel
from typing import Optional 


class User(BaseModel):
    username: str
    password: str
    email: str
    description: str


class UserInDB(User):
    user_id: int
    is_active: bool
    is_verified: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

