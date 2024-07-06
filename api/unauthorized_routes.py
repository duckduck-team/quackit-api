from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.posts import post_utils
from api.schemas import post_schemas
from api.postgresql.db import get_db


router = APIRouter(
    prefix="/post",
    tags=["Unauthorized endpoints"],
    dependencies=[Depends(get_db)]
)

@router.get(
    "/post/{post_id}",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/{post_id}` shows one post""",
)
async def one_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> post_schemas.PostInDB:
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post does not exist")
    return db_post


@router.get(
    "/postlist_all",
    response_model=post_schemas.AvailablePosts,
    status_code=200,
    summary="""The endpoint `/postlist_all` shows all created posts""",
)
async def all_posts(
    db: Session = router.dependencies[0],
):
    return {"posts": db.query(models.Post).all()}