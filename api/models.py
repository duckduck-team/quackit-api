from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Table
from api.postgresql.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    description = Column(Text, default="")

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    post_votes = relationship("PostVote", back_populates="user")
    comment_votes = relationship("CommentVote", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    votes_count = Column(Integer, default=0)
    published_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    post_votes = relationship("PostVote", back_populates="post")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")


class Comment(Base):
    __tablename__ = "comments"
    
    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id", ondelete="CASCADE"), nullable=True)
    content = Column(Text, nullable=False)
    votes_count = Column(Integer, default=0)
    published_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    comment_votes = relationship("CommentVote", back_populates="comment")
    parent_comment = relationship("Comment", remote_side=[comment_id], backref=backref("replies", lazy="dynamic"))


class PostVote(Base):
    __tablename__ = "post_votes"
    
    post_vote_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="post_votes")
    post = relationship("Post", back_populates="post_votes")


class CommentVote(Base):
    __tablename__ = "comment_votes"
    
    comment_vote_id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.comment_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="comment_votes")
    comment = relationship("Comment", back_populates="comment_votes")


class Tag(Base):
    __tablename__ = "tags"
    
    tag_id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, nullable=False)
    
    posts = relationship("Post", secondary="post_tags", back_populates="tags")


class PostTag(Base):
    __tablename__ = "post_tags"
    
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id"), primary_key=True)
    published_at = Column(DateTime, default=datetime.utcnow)
