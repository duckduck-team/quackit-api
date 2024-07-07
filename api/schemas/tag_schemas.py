from pydantic import BaseModel
from typing import List


class Tag(BaseModel):
    tag: str


class TagUID(BaseModel):
    tag: str
    post_id: int


class TagInDB(Tag):
    tag_id: int


class PostTag(BaseModel):
    tag_id: int
    post_id: int


class AvailavbleTags(BaseModel):
    tags: List[TagInDB]
