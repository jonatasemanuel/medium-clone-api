from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    bio: str
    image: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class TagSchema(BaseModel):
    slug: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ArticleSchema(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    # tag: list[TagSchema]


class ArticleInput(ArticleSchema):
    tag_slug: str
    article: ArticleSchema
