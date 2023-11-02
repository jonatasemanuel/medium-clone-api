from slugify import slugify
from sqlalchemy import func, select

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Article, Tag, TagArticle, User
from api.db.schemas import ArticleInput, ArticleSchema, TagSchema
from api.routes.user import CurrentUser, get_profile

from api.security import get_current_user_optional

from api.db.schemas import (
    Profile,
    Message,
)

router = APIRouter(prefix='/api/articles', tags=['articles'])
Session = Annotated[Session, Depends(get_session)]


@ router.post('/', response_model=ArticleSchema, status_code=201)
def create_article(
    article: ArticleInput,
    current_user: CurrentUser,
    session: Session,
    # tag_list: Optional[list] = [],
):
    slug = slugify(article.title)

    article_name = session.scalar(select(Article).where(Article.slug == slug))
    if article_name:
        raise HTTPException(
            status_code=400, detail="Article title already used")

    db_article: Article = Article(
        slug=slug,
        title=article.title,
        description=article.description,
        body=article.body,
        created_at=func.now(),
        updated_at=func.now(),
        author=current_user,
    )

    if article.tag_list is not None:
        for tag in article.tag_list:
            tags_to_link = session.scalar(select(TagArticle).where(
                TagArticle.tag_name == tag, TagArticle.article_slug == slug))
            if tags_to_link:
                raise HTTPException(status_code=400, detail="Tag already attr")

            tag = TagArticle(article_slug=slug, tag_name=slugify(tag))

            session.add(tag)
            session.commit()
            session.refresh(tag)

    tags = session.scalars(select(TagArticle).where(
        TagArticle.article_slug == slug)).all()

    db_article.tag_list = tags

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    author_profile = get_profile(
        username=db_article.author.username,
        session=session,
        current_user=current_user
    )

    article_response: ArticleSchema = ArticleSchema(
        slug=db_article.slug,
        title=db_article.title,
        description=db_article.description,
        body=db_article.body,
        # ARRUMAR UMA FORMA DE PASSAR EM FORDA DE DICIONARIO
        tag_list=article.tag_list,
        created_at=db_article.created_at,
        updated_at=db_article.updated_at,
        author=author_profile,
    )

    return article_response
