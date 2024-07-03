from sqlalchemy.orm import Session
from api import models
from api.schemas import post_schemas


# depend on user_id
async def get_post(
    db: Session,
    title: str,
    user_id: str,
) -> post_schemas.PostInDB:
    return db.query(models.Post).filter(
        models.Post.title == title,
        models.Post.user_id == user_id
    ).first()


# do not depend on user_id
async def get_any_post(
    db: Session,
    title: str,
) -> post_schemas.PostInDB:
    return db.query(models.Post).filter(models.Post.title == title).first()


async def get_vote(
    db: Session,
    post_id: str,
    user_id: str,
) -> post_schemas.PostInDB:
    return db.query(models.PostVote).filter(
        models.PostVote.post_id == post_id,
        models.PostVote.user_id == user_id
    ).first()