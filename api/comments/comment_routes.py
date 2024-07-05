from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.comments import comment_utils
from api.schemas import comment_schemas, user_schemas
from api.postgresql.db import get_db

USER = 0
SESSION = 1

router = APIRouter(
    prefix="/comment",
    tags=["Comment Maintenance"],
    dependencies=[Depends(auth.get_current_user), Depends(get_db)]
)

@router.post(
    "/create",
    response_model=comment_schemas.CommentInDB,
    status_code=200,
    summary="""The endpoint `/create` create a new comment for the post.""",
)
async def create(
        comment: comment_schemas.Comment,
        current_user: user_schemas.UserInDB = router.dependencies[USER],
        db: Session = router.dependencies[SESSION],
):
    db_comment: comment_schemas.CommentInDB = await comment_utils.get_comment(
        db,
        post_id=comment.post_id,
        user_id=current_user.user_id
    )
    if db_comment:
        raise HTTPException(status_code=400, detail=f"Comment for this post already created")


    db_comment = models.Comment(
        user_id=current_user.user_id,
        post_id=comment.post_id,
        content=comment.content
    )

    db.add(db_comment)
    db.commit()

    return db_comment