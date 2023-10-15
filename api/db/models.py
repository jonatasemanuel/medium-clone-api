from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[Optional[int]] = mapped_column(default=None, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    bio: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    articles: Mapped[list['Article']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    # following_id: Optional[list['Following']] = Field(foreign_key='user.id')


class Article(Base):
    __tablename__ = "articles"

    slug: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    body: Mapped[str]

    # tag_slug: Mapped[Optional[str]] = mapped_column(ForeignKey("tags.slug"))
    # tag: Mapped["Tag"] = relationship(back_populates='articles')

    # created_at: Mapped[DateTime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[DateTime] = mapped_column(onupdate=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # favorited_users_id: Optional[list] = None
    user: Mapped[User] = relationship(back_populates='articles')


class Tag(Base):
    __tablename__ = "tags"

    slug: Mapped[str] = mapped_column(primary_key=True)

    # article_slug: Mapped[Optional[str]] = mapped_column(
    #   ForeignKey("articles.slug"))
    # articles: Mapped[List["Article"]] = relationship(back_populates="tag")


"""
class Following(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key='user.id')
"""
