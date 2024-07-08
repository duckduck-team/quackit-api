from pydantic import BaseModel


class PostVote(BaseModel):
    post_id: int


class PostVoteInDB(PostVote):
    post_vote_id: int
    user_id: int
    value: int


class CommentVote(BaseModel):
    comment_id: int


class CommentVoteInDB(CommentVote):
    comment_vote_id: int
    user_id: int
    value: int