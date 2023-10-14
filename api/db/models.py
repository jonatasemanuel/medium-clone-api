from datetime import datetime
from fastapi import FastAPI

from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Relationship
# Session
# from pydantic import ConfigDict, EmailStr, root_validator




"""class Article(SQLModel, table=True):
    slug: Optional[str] = Field(default=None, primary_key=True)

    title: str
    description: str
    body: str
    tag_list: Optional[list['Tag']] = Relationship(back_populates='tags')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # author: int = Field(foreign_key='user.id')
    # favorited_users_id: Optional[list] = None
    # user: Optional[list['User']] = Relationship(back_populates='articles')
"""

class Tag(SQLModel, table=True):
    slug: str = Field(default=None, primary_key=True)

    # article: Optional[list['Article']] = Relationship(
    #    back_populates='articles')

"""
class Following(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key='user.id')

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    bio: Optional[str] = None
    image: Optional[str] = None

    articles: Optional[list['Article']] = Relationship(back_populates='user')
    following_id: Optional[list['Following']] = Field(foreign_key='user.id')
"""
