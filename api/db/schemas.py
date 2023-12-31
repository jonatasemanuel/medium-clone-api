from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from api.db.models import Article, User


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}
        return d


class UserSchema(CustomBaseModel):
    # id: int
    username: str
    email: EmailStr
    password: str
    bio: str
    image: str


class UserDB(UserSchema):
    id: int


class UserPublic(CustomBaseModel):
    # id: int
    email: EmailStr
    username: str
    bio: str
    image: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(CustomBaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    bio: str | None = None
    image: str | None = None


class Profile(UserPublic):
    following: bool = False


class UserPrivate(UserPublic):
    token: str


class UserList(CustomBaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class TagSchema(CustomBaseModel):
    name: str


class CommentSchema(CustomBaseModel):
    body: str


class ArticleUpdate(CustomBaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None
    tag_list: Optional[list[str]] | None = None


class ArticleSchema(CustomBaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: Optional[list[str]] = []
    created_at: datetime
    updated_at: datetime
    author: Profile


class PublicArticleSchema(CustomBaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: Optional[list[str]] = []
    created_at: datetime
    updated_at: datetime
    favorited: bool = False
    favorites_count: int
    author: Profile


class MultArticle(CustomBaseModel):
    articles: list[PublicArticleSchema]
    articles_count: int


class ArticleInput(CustomBaseModel):
    title: str
    description: str
    body: str
    tag_list: Optional[list[str]] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
