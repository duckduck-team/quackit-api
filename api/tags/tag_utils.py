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
