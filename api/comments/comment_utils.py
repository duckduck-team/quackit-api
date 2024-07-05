from sqlalchemy.orm import Session
from api import models
from api.schemas import comment_schemas


# depend on user_id
async def get_comment(
    db: Session,
    user_id: str,
    post_id: str,
) -> comment_schemas.CommentInDB:
    return db.query(models.Comment).filter(
        models.Comment.user_id == user_id,
        models.Comment.post_id == post_id
    ).first()