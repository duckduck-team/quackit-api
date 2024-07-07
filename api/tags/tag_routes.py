from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.tags import tag_utils
from api.posts import post_utils
from api.schemas import tag_schemas, user_schemas, post_schemas
from api.postgresql.db import get_db

USER = 0
SESSION = 1

router = APIRouter(
    prefix="/tag",
    tags=["Tag Maintenance"],
    dependencies=[Depends(auth.get_current_user), Depends(get_db)]
)

@router.post(
    "/add_or_create_tag",
    response_model=tag_schemas.TagInDB,
    status_code=200,
    summary="""The endpoint '/add_or_create_tag' adds a new/existing tag to a post."""
)
async def add_or_create_tag(
    tag_add: tag_schemas.TagUID,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION]
) -> tag_schemas.TagInDB:
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=tag_add.post_id
    )
    if not db_post:
        raise HTTPException(status_code=404, detail="Post does not exist")
    
    if db_post.user_id != current_user.user_id:
        raise HTTPException(status_code=401, detail="You can only add tags to your own posts")

    db_tag: tag_schemas.TagInDB = await tag_utils.get_one_tag(db, tag=tag_add.tag)
    if not db_tag:
        db_tag = models.Tag(tag=tag_add.tag)
        db.add(db_tag)
        db.commit()
    
    post_tag: tag_schemas.PostTag = await tag_utils.get_post_tag(
        db,
        tag_id=db_tag.tag_id,
        post_id=db_post.post_id
    )
    if post_tag:
        raise HTTPException(status_code=400, detail="Tag already added for this post")

    post_tag: tag_schemas.PostTag = models.PostTag(
        post_id=db_post.post_id,
        tag_id=db_tag.tag_id
    )

    db.add(post_tag)
    db.commit()
    return db_tag

@router.delete(
    "/delete",
    response_model=tag_schemas.TagInDB,
    status_code=200,
    summary="""The endpoint '/delete' deletes an existing tag from a post."""
)
async def delete(
    tag_delete: tag_schemas.TagUID,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION]
) -> tag_schemas.TagInDB:
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=tag_delete.post_id
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")
    
    if db_post.user_id != current_user.user_id:
        raise HTTPException(status_code=401, detail="You can delete tags only from your own posts")

    db_tag: tag_schemas.TagInDB = await tag_utils.get_one_tag(
        db,
        tag=tag_delete.tag
    )
    if not db_tag:
        raise HTTPException(status_code=400, detail="Tag does not exists")

    db_post_tag: tag_schemas.TagInDB = await tag_utils.get_post_tag(
        db,
        tag_id=db_tag.tag_id,
        post_id=tag_delete.post_id
    )
    if not db_post_tag:
        raise HTTPException(status_code=400, detail="Such tag does not exists for this post")

    db.delete(db_post_tag)
    db.commit()

    return db_tag
