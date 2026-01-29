from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_user = Table(
    "follower_user",
    db.metadata,
    Column("user_from", ForeignKey("user.id")),
    Column("user_to", ForeignKey("follower.id"))
)


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[List["User"]] = relationship(
        secondary="follower_user", back_populates="follower")


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user_comment")
    posts: Mapped[List["Post"]] = relationship(back_populates="user_post")
    follower: Mapped[List["Follower"]] = relationship(
        secondary="follower_user", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "comments": [comment.serialize() for comment in self.comments],
            "posts": [post.serialize() for post in self.posts]
            # do not serialize the password, its a security breach
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(
        String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_comment: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    comments_for_post: Mapped["Post"] = relationship(
        back_populates="post_comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_post: Mapped["User"] = relationship(back_populates="posts")
    post_comments: Mapped[List["Comment"]] = relationship(
        back_populates="comments_for_post")
    post_media: Mapped[List["Media"]] = relationship(
        back_populates="media_in_post")

    def serialize(self):
        return {
            "id": self.id
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        String(120),  nullable=False)
    url: Mapped[str] = mapped_column(
        String(255), unique=False, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    media_in_post: Mapped["Post"] = relationship(back_populates="post_media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url
        }
