from slugify import slugify
from sqlalchemy import func, select

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Article, User
from api.db.schemas import ArticleInput, ArticleSchema, TagSchema
from api.routes.user import CurrentUser, get_profile

from api.security import (
    get_current_user,
    get_current_user_optional,
)

from api.db.schemas import (
    Profile,
    Message,
)

router = APIRouter(prefix='/api/articles', tags=['articles'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=ArticleSchema, status_code=201)
def create_article(
    article: ArticleInput,
    current_user: CurrentUser,
    session: Session
):
    """
    - [ ] Verificação da tag no banco de dados (optional), rodar verificaçao
          com for para cada item passado na lista
    """
    # for tag in article.tag_list
    # tag = session.scalar(select(Tag).where(Tag.slug == tag))

    # tag_slug on func request, and add tag
    db_article: Article = Article(
        slug=slugify(article.title),
        title=article.title,
        description=article.description,
        body=article.body,
        # tag_list=article.tag_list,
        created_at=func.now(),
        updated_at=func.now(),
        author=current_user,
    )
    author_profile = get_profile(
        username=db_article.author.username,
        session=session,
        current_user=current_user
    )

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    article_response: ArticleSchema = ArticleSchema(
        slug=db_article.slug,
        title=db_article.title,
        description=db_article.description,
        body=db_article.body,
        # tag_list=article.tag_list,
        created_at=db_article.created_at,
        updated_at=db_article.updated_at,
        author=author_profile,
    )

    return article_response
