from pydantic import BaseModel
from typing import List
from datetime import datetime

class Comment(BaseModel):
    content: str
    parent_comment_id: int | None
    post_id: int

class CommentInDB(Comment):
    user_id: int
    votes_count: int
    published_at: datetime
