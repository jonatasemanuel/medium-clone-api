from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Article
from api.db.schemas import ArticleSchema


Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/api/article', tags=['articles'])


@router.post('/', response_model=ArticleSchema, status_code=201)
def create_article(
    article: ArticleSchema,
    session: Session,
):
    db_article = Article(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
    )

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    return db_article
