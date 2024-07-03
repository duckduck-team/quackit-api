from pydantic import BaseModel
from typing import List
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str


class PostInDB(Post):
    post_id: int
    user_id: int
    votes_count: int
    published_at: datetime


class PostToRemove(BaseModel):
    title: str


class AvailablePosts(BaseModel):
    posts: List[PostInDB]