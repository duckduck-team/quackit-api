from sqlalchemy.orm import Session
from api import models
from api.schemas import vote_schemas


async def get_vote(
    db: Session,
    post_id: int,
    user_id: int,
) -> vote_schemas.PostVoteInDB:
    return db.query(models.PostVote).filter(
        models.PostVote.post_id == post_id,
        models.PostVote.user_id == user_id
    ).first()


async def get_votes(
    db: Session,
    post_id: int,
) -> vote_schemas.PostVoteInDB:
    return db.query(models.PostVote).filter(
        models.PostVote.post_id == post_id,
    ).all()


async def delete_comets_from_post(
    db: Session,
    post_id: int,
) -> None:
    db_post_votes: vote_schemas.PostVoteInDB = await get_votes(
        db,
        post_id=post_id
    )
    for post_vote in db_post_votes:
        db.delete(post_vote)
