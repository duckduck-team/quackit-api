from api.postgresql.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.votes import vote_utils
from api.posts import post_utils
from api.schemas import post_schemas, user_schemas, vote_schemas
from api.postgresql.db import get_db

USER = 0
SESSION = 1

router = APIRouter(
    prefix="/vote",
    tags=["Vote Maintenance"],
    dependencies=[Depends(auth.get_current_user), Depends(get_db)]
)


@router.post(
    "/vote_for",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/vote_for` allows particular user to vote for some post.""",
)
async def vote_for(
    vote: vote_schemas.PostVote,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
) -> post_schemas.PostInDB:
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=vote.post_id,
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")

    db_vote: vote_schemas.PostVoteInDB = await vote_utils.get_vote(
        db,
        post_id=db_post.post_id,
        user_id=current_user.user_id
    )
    if db_vote:
        if db_vote.value == -1:
            db_post.votes_count += 2
            db_vote.value = 1
        else:
            db.delete(db_vote)
            db_post.votes_count -= 1
    else:
        db_vote = models.PostVote(
            post_id=db_post.post_id,
            user_id=current_user.user_id,
            value=1
        )
        db.add(db_vote)
        db_post.votes_count += 1

    db.commit()
    return db_post


@router.post(
    "/vote_against",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="""The endpoint `/vote_against` allows particular user to vote against some post.""",
)
async def vote_against(
    vote: vote_schemas.PostVote,
    current_user: user_schemas.UserInDB = router.dependencies[USER],
    db: Session = router.dependencies[SESSION],
) -> post_schemas.PostInDB:
    db_post: post_schemas.PostInDB = await post_utils.get_one_post(
        db,
        post_id=vote.post_id,
    )
    if not db_post:
        raise HTTPException(status_code=400, detail="Post does not exists")

    db_vote: vote_schemas.PostVoteInDB = await vote_utils.get_vote(
        db,
        post_id=db_post.post_id,
        user_id=current_user.user_id
    )
    if db_vote:
        if db_vote.value == -1:
            db.delete(db_vote)
            db_post.votes_count += 1
        else:
            db_vote.value = -1
            db_post.votes_count -= 2
    else:
        db_vote = models.PostVote(
            post_id=db_post.post_id,
            user_id=current_user.user_id,
            value=-1
        )
        db.add(db_vote)
        db_post.votes_count -= 1

    db.commit()
    return db_post