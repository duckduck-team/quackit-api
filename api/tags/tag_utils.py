from sqlalchemy.orm import Session
from api import models
from api.schemas import tag_schemas


async def get_one_tag(
    db: Session,
    tag: str,
) -> tag_schemas.TagInDB:
    return db.query(models.Tag).filter(models.Tag.tag == tag).first()


async def get_post_tag(
    db: Session,
    tag_id: int,
    post_id: int,
) -> tag_schemas.TagInDB:
    return db.query(models.PostTag).filter(
        models.PostTag.tag_id == tag_id,
        models.PostTag.post_id == post_id
    ).first()


async def get_tags(
    db: Session,
    post_id: int,
) -> tag_schemas.PostTag:
    return db.query(models.PostTag).filter(
        models.PostTag.post_id == post_id,
    ).all()


async def delete_comets_from_post(
    db: Session,
    post_id: int,
) -> None:
    db_post_tags: tag_schemas.PostTag = await get_tags(
        db,
        post_id=post_id
    )
    for post_tag in db_post_tags:
        db.delete(post_tag)
