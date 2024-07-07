from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.posts import post_utils
from api.tags import tag_utils
from api.schemas import post_schemas, tag_schemas
from api.postgresql.db import get_db


router = APIRouter(
    prefix="/unauthorized",
    tags=["Unauthorized endpoints"],
    dependencies=[Depends(get_db)]
)

@router.get(
    "/post/{post_id}",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/post/{post_id}` shows one post""",
)
async def one_post(
    post_id: int,
    db: Session = router.dependencies[0],
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
) -> post_schemas.AvailablePosts:
    return {"posts": db.query(models.Post).all()}

@router.get(
    "/tags_all",
    response_model=tag_schemas.AvailavbleTags,
    status_code=200,
    summary="""The endpoint `/tags_all` shows all created tags""",
)
async def all_tags(
    db: Session = router.dependencies[0],
) -> tag_schemas.AvailavbleTags:
    return {"tags": db.query(models.Tag).all()}

@router.get(
    "/tag/{tag_title}",
    response_model=tag_schemas.TagInDB,
    status_code=200,
    summary="""The endpoint `/tag/{tag_title}` shows one tag""",
)
async def one_tag(
    tag_title: str,
    db: Session = router.dependencies[0],
) -> tag_schemas.TagInDB:
    db_tag: tag_schemas.TagInDB = await tag_utils.get_one_tag(db, tag=tag_title)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag does not exist")
    return db_tag

