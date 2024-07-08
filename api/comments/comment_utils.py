from sqlalchemy.orm import Session
from api import models
from api.schemas import comment_schemas


async def get_comment_by_uid(
    db: Session,
    comment_id: int
) -> comment_schemas.CommentInDB:
    return db.query(models.Comment).filter(
        models.Comment.comment_id == comment_id
    ).first()


async def get_comment(
    db: Session,
    user_id: int,
    post_id: int,
    parent_comment_id: int,
    content: str
) -> comment_schemas.CommentInDB:
    return db.query(models.Comment).filter(
        models.Comment.user_id == user_id,
        models.Comment.post_id == post_id,
        models.Comment.content == content,
        models.Comment.parent_comment_id == parent_comment_id
    ).first()


async def get_comments_for_post(
    db: Session,
    post_id: int,
) -> comment_schemas.CommentInDB:
    return db.query(models.Comment).filter(
        models.Comment.post_id == post_id,
    ).all()


async def delete_comets_from_post(
    db: Session,
    post_id: int,
) -> None:
    db_comments: comment_schemas.CommentInDB = await get_comments_for_post(
        db,
        post_id=post_id
    )
    for comment in db_comments:
        db.delete(comment)
