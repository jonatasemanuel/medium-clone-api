from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Follow(Base):
    __tablename__ = 'association_table'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey('followings.id'), primary_key=True
    )
    following: Mapped['Following'] = relationship(back_populates='users')
    user: Mapped['User'] = relationship(back_populates='following')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    bio: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    following: Mapped[List['Follow']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    articles: Mapped[List['Article']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )
    comments: Mapped[List['Comment']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )


class Following(Base):
    __tablename__ = 'followings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    users: Mapped[List['Follow']] = relationship(back_populates='following')


class TagArticle(Base):
    __tablename__ = 'tags_article'

    article_slug: Mapped[str] = mapped_column(
        ForeignKey('articles.slug'), primary_key=True
    )
    tag_name: Mapped[str] = mapped_column(
        ForeignKey('tags.name'), primary_key=True
    )
    articles: Mapped['Article'] = relationship(back_populates='tag_list')
    tag: Mapped['Tag'] = relationship(back_populates='articles')


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(default=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(default=None, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    tag_list: Mapped[Optional[List['TagArticle']]] = relationship(
        back_populates='articles', cascade='all, delete-orphan'
    )
    favorited: Mapped[List['Favorites']] = relationship(
        back_populates='article', cascade='all, delete-orphan'
    )
    author: Mapped[User] = relationship(back_populates='articles')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    comments: Mapped[List['PostComment']] = relationship(
        back_populates='article', cascade='all, delete-orphan'
    )


class Tag(Base):
    __tablename__ = 'tags'

    name: Mapped[str] = mapped_column(default=None, primary_key=True)
    articles: Mapped[List['TagArticle']] = relationship(
        back_populates='tag', cascade='all, delete-orphan'
    )


class Favorites(Base):
    __tablename__ = 'favorite_association'

    # article_slug: Mapped[str] = mapped_column(
    #     ForeignKey("articles.slug"), primary_key=True
    # )
    article_id: Mapped[str] = mapped_column(
        ForeignKey('articles.id'), primary_key=True
    )
    favorited_by_user: Mapped[str] = mapped_column(
        ForeignKey('favorited.username'), primary_key=True
    )
    # article_id: Mapped[int]

    favorited: Mapped['Favorited'] = relationship(back_populates='articles')

    article: Mapped['Article'] = relationship(back_populates='favorited')


class Favorited(Base):
    __tablename__ = 'favorited'

    username: Mapped[str] = mapped_column(primary_key=True, index=True)

    articles: Mapped[List['Favorites']] = relationship(
        back_populates='favorited', cascade='all, delete-orphan'
    )


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    comments: Mapped[List['PostComment']] = relationship(
        back_populates='comment', cascade='all, delete-orphan'
    )
    author: Mapped['User'] = relationship(back_populates='comments')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class PostComment(Base):
    __tablename__ = 'comment_association'
    article_slug: Mapped[str] = mapped_column(
        ForeignKey('articles.slug'), primary_key=True
    )
    article: Mapped['Article'] = relationship(back_populates='comments')

    comment_id: Mapped[int] = mapped_column(
        ForeignKey('comments.id'), primary_key=True
    )
    comment: Mapped['Comment'] = relationship(back_populates='comments')
