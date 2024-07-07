from pydantic import BaseModel


class PostVote(BaseModel):
    post_id: int


class PostVoteInDB(PostVote):
    post_vote_id: int
    user_id: int
    value: int