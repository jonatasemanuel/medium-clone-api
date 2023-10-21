"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import op

from api.db.database import get_session
from api.db.models import Article
from api.db.schemas import ArticleInput, ArticleSchema
from api.routes.user import CurrentUser


Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/api/article', tags=['articles'])


@router.post('/', response_model=ArticleInput, status_code=201)
def create_article(
    article: ArticleSchema,
    user: CurrentUser,
    session: Session,
):
    # tag_slug on func request, and add tag
    db_article: Article = Article(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        user_id=user.id
    )

    # db_article = Article(tags=tag.slug)

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    return db_article
"""
