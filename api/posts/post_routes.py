from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.schemas import post_schemas, user_schemas
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
    summary="""The endpoint `/create` create a new post for particular user.""",
)
async def create(
        post: post_schemas.Post,
        current_user: user_schemas.UserInDB = router.dependencies[USER],
        db: Session = router.dependencies[SESSION],
):
    db_post: post_schemas.PostInDB = await auth.get_post(
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


@router.post(
    "/remove",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/remove` remove a post for particular user.""",
)
async def remove(
    post: post_schemas.PostToRemove,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    db_post: post_schemas.PostInDB = await auth.get_post(
        db,
        title=post.title,
        user_id=current_user.user_id
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")


    db.delete(db_post)
    db.commit()

    return db_post


@router.get(
    "/postlist",
    response_model=post_schemas.AvailablePosts,
    status_code=200,
    summary="""The endpoint `/postlist` shows all posts from a particular user.""",
)
async def current_databases(
        user: user_schemas.UserInDB = router.dependencies[USER],
        db: Session = router.dependencies[SESSION],
):
    return {"posts": db.query(models.Post).filter(models.Post.user_id == user.user_id).all()}
