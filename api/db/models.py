from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, Table, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_following = Table(
    'user_following',
    Base.metadata,
    Column('user_id', Integer, ForeignKey("users.id"), primary_key=True),
    Column('following_id', Integer, ForeignKey("users.id"), primary_key=True)
)


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    bio: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    following: Mapped[Optional[List["User"]]] = relationship(
        "User",
        secondary=user_following,
        primaryjoin=id == user_following.c.user_id,
        secondaryjoin=id == user_following.c.following_id,
        back_populates='following'
    )
    #               ] = relationship(secondary=association_table)

    # articles: Mapped[list['Article']] = relationship(
    #    back_populates='author', cascade='all, delete-orphan')


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


class Following(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key='user.id')
"""
