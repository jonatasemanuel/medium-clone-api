from datetime import datetime
from fastapi import FastAPI

from decouple import config
from sqlalchemy import create_engine

from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Relationship
# Session
# from pydantic import ConfigDict, EmailStr, root_validator


# Connection
DB_URL = config('DB_URL')
engine = create_engine(DB_URL)
SQLModel.metadata.create_all(engine)

app = FastAPI()


class Article(SQLModel, table=True):
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


class Tag(SQLModel, table=True):
    slug: Optional[str] = Field(default=None, primary_key=True)

    article: Optional[list['Article']] = Relationship(
        back_populates='articles')
