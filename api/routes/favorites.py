from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Article, Favorites, Follow, TagArticle
from api.db.schemas import PublicArticleSchema  # Message,
from api.routes.article import get_article
from api.routes.user import CurrentUser

router = APIRouter(prefix='/api/articles', tags=['Favorites'])
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/{slug}/favorite', response_model=PublicArticleSchema, status_code=201
)
def favorite_article(session: Session, current_user: CurrentUser, slug: str):
    article = session.scalar(select(Article).where(Article.slug == slug))
    if not article:
        raise HTTPException(status_code=404, detail='Article not exist')
    article_to_favorite = session.scalar(
        select(Favorites).where(
            Favorites.favorited_by_user == current_user.username,
            Favorites.article_id == article.id,
        )
    )

    if article_to_favorite:
        raise HTTPException(
            status_code=400, detail='Article already favorited'
        )
    favorite: Favorites = Favorites(
        favorited_by_user=current_user.username,
        article_id=article.id,
    )

    session.add(favorite)
    session.commit()
    session.refresh(favorite)

    fav_article = get_article(slug, session)
    fav_article.favorited = True

    user_to_check = session.scalar(
        select(Follow).where(
            Follow.following_id == article.user_id,
            Follow.user_id == current_user.id,
        )
    )

    if user_to_check:
        fav_article.author.following = True

    return fav_article


@router.delete(
    '/{slug}/favorite', response_model=PublicArticleSchema, status_code=201
)
def unfavorite_article(session: Session, current_user: CurrentUser, slug: str):
    article = session.scalar(select(Article).where(Article.slug == slug))
    if not article:
        raise HTTPException(status_code=404, detail='Article not exist')

    article_to_unfavorite = session.scalar(
        select(Favorites).where(
            Favorites.favorited_by_user == current_user.username,
            Favorites.article_slug == article.slug,
        )
    )
    if not article_to_unfavorite:
        raise HTTPException(status_code=400, detail='Article is not favorited')

    session.delete(article_to_unfavorite)
    session.commit()

    fav_article = get_article(slug, session)

    user_to_check = session.scalar(
        select(Follow).where(
            Follow.following_id == article.user_id,
            Follow.user_id == current_user.id,
        )
    )

    if user_to_check:
        fav_article.author.following = True

    return fav_article
