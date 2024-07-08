from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.posts import post_utils
from api.votes import vote_utils
from api.tags import tag_utils
from api.comments import comment_utils
from api.schemas import post_schemas, user_schemas, tag_schemas, vote_schemas, comment_schemas
from api.postgresql.db import get_db

USER = 0
SESSION = 1

router = APIRouter(
    prefix="/post",
    tags=["Post Maintenance"],
    dependencies=[Depends(auth.get_current_user), Depends(get_db)]
)

@router.post(
    "/create",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/create` create a new post for current logged user.""",
)
async def create(
    post: post_schemas.Post,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    db_post: post_schemas.PostInDB = await post_utils.create_post(
        db,
        title=post.title,
        user_id=current_user.user_id
    )
    if db_post:
        raise HTTPException(status_code=400, detail=f"Post already created")

    db_post = models.Post(
        user_id=current_user.user_id,
        title=post.title,
        content=post.content
    )

    db.add(db_post)
    db.commit()

    return db_post


@router.delete(
    "/delete",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/delete` remove a post for current logged user.""",
)
async def delete(
    post: post_schemas.PostUID,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=post.post_id
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")
    
    if db_post.user_id != current_user.user_id:
        raise HTTPException(status_code=401, detail="You can delete only your own posts")
    
    await comment_utils.delete_comets_from_post(db, db_post.post_id)

    await vote_utils.delete_comets_from_post(db, post_id=db_post.post_id)

    await tag_utils.delete_comets_from_post(db, post_id=db_post.post_id)

    db.delete(db_post)
    db.commit()

    return db_post


@router.get(
    "/postlist_current",
    response_model=post_schemas.AvailablePosts,
    status_code=200,
    summary="""The endpoint `/postlist_current` shows all posts created by the current logged user.""",
)
async def my_posts(
    user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    return {"posts": db.query(models.Post).filter(models.Post.user_id == user.user_id).all()}
