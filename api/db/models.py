from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Follow(Base):
    __tablename__ = "association_table"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    following_id: Mapped[int] = mapped_column(
        ForeignKey("followings.id"), primary_key=True)

    following: Mapped["Following"] = relationship(
        back_populates="users")

    user: Mapped["User"] = relationship(
        back_populates="following")


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    bio: Mapped[Optional[str]]
    image: Mapped[Optional[str]]

    following: Mapped[List["Follow"]] = relationship(back_populates="user")


class Following(Base):
    __tablename__ = "followings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    users: Mapped[List["Follow"]] = relationship(back_populates="following")


"""
class Article(Base):
    __tablename__ = "articles"

    id: Mapped[Optional[int]] = mapped_column(default=None)
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    body: Mapped[str]

    # tag_slug: Mapped[Optional[str]] = mapped_column(ForeignKey("tags.slug"))
    # tag: Mapped["Tag"] = relationship(back_populates='articles')

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # favorited_users_id: Optional[list] = None
    author: Mapped[User] = relationship(back_populates='articles')



class Tag(Base):
    __tablename__ = "tags"

    slug: Mapped[str] = mapped_column(primary_key=True)

    # article_slug: Mapped[Optional[str]] = mapped_column(
    #   ForeignKey("articles.slug"))
    # articles: Mapped[List["Article"]] = relationship(back_populates="tag")

"""
