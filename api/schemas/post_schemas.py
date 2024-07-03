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


class PostUID(BaseModel):
    title: str


class AvailablePosts(BaseModel):
    posts: List[PostInDB]


class VoteInDB(BaseModel):
    vote_id: int
    user_id: int
    post_id: int