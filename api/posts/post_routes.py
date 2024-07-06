from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.posts import post_utils
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
    db_post: post_schemas.PostInDB = await post_utils.get_post_to_delete(
        db,
        post_id=post.post_id,
        user_id=current_user.user_id
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")

    db_post_votes = db.query(models.PostVote).filter_by(post_id=db_post.post_id).all()
    for post_vote in db_post_votes:
        db.delete(post_vote)

    db.delete(db_post)
    db.commit()

    return db_post


@router.post(
    "/vote",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/vote` allows particular user vote for some post.""",
)
async def vote(
    post: post_schemas.PostUID,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=post.post_id,
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")

    db_vote: post_schemas.VoteInDB = await post_utils.get_vote(
        db,
        post_id=db_post.post_id,
        user_id=current_user.user_id
    )
    if db_vote:
        db.delete(db_vote)
        db_post.votes_count -= 1
    else:
        db_vote = models.PostVote(
            post_id=db_post.post_id,
            user_id=current_user.user_id
        )
        db.add(db_vote)
        db_post.votes_count += 1

    db.commit()
    return db_post


@router.get(
    "/postlist_current",
    response_model=post_schemas.AvailablePosts,
    status_code=200,
    summary="""The endpoint `/postlist_current` shows all created posts""",
)
async def my_posts(
    user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
):
    return {"posts": db.query(models.Post).filter(models.Post.user_id == user.user_id).all()}
