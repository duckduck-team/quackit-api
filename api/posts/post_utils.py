from sqlalchemy.orm import Session
from api import models
from api.schemas import post_schemas, tag_schemas


async def create_post(
    db: Session,
    title: str,
    user_id: int
) -> post_schemas.PostInDB:
    return db.query(models.Post).filter(
        models.Post.title == title,
        models.Post.user_id == user_id
    ).first()


async def get_one_post(
    db: Session,
    post_id: int,
) -> post_schemas.PostInDB:
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()


async def get_vote(
    db: Session,
    post_id: int,
    user_id: int,
) -> post_schemas.PostInDB:
    return db.query(models.PostVote).filter(
        models.PostVote.post_id == post_id,
        models.PostVote.user_id == user_id
    ).first()

async def get_votes(
    db: Session,
    post_id: int,
) -> post_schemas.PostInDB:
    return db.query(models.PostVote).filter(
        models.PostVote.post_id == post_id,
    ).all()


async def get_tags(
    db: Session,
    post_id: int,
) -> tag_schemas.PostTag:
    return db.query(models.PostTag).filter(
        models.PostTag.post_id == post_id,
    ).all()

