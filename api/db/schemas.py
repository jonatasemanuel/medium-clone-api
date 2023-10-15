from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class TagSchema(BaseModel):
    slug: str


class ArticleSchema(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    # tag: list[TagSchema]


class ArticleInput(ArticleSchema):
    tag_slug: str
    article: ArticleSchema
