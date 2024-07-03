from pydantic import BaseModel
from typing import Optional, List, Dict


class User(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

