from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import func, join, select
from sqlalchemy.orm import Bundle, Session

from api.db.database import get_session
from api.db.models import Article, Favorites, Follow, Following, TagArticle, User
from api.db.schemas import (
    ArticleInput,
    ArticleSchema,
    Message,
    MultArticle,
    Profile,
)
from api.routes.user import CurrentUser, get_profile
from api.security import get_current_user_optional

router = APIRouter(prefix='/api/articles', tags=['articles'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=ArticleSchema, status_code=201)
def create_article(
    article: ArticleInput,
    current_user: CurrentUser,
    session: Session,
):
    slug = slugify(article.title)

    article_name = session.scalar(select(Article).where(Article.slug == slug))
    if article_name:
        raise HTTPException(
            status_code=400, detail='Article title already used'
        )

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
            tags_to_link = session.scalar(
                select(TagArticle).where(
                    TagArticle.tag_name == tag, TagArticle.article_slug == slug
                )
            )
            if tags_to_link:
                raise HTTPException(
                    status_code=400, detail=f"Tag '{tag}' is duplicated"
                )

            tag = TagArticle(article_slug=slug, tag_name=slugify(tag))

            session.add(tag)
            session.commit()
            session.refresh(tag)

    tags = session.scalars(
        select(TagArticle).where(TagArticle.article_slug == slug)
    ).all()

    db_article.tag_list = tags

    session.add(db_article)
    session.commit()
    session.refresh(db_article)

    author_profile = get_profile(
        username=db_article.author.username,
        session=session,
        current_user=current_user,
    )

    article_response: ArticleSchema = ArticleSchema(
        slug=db_article.slug,
        title=db_article.title,
        description=db_article.description,
        body=db_article.body,
        tag_list=article.tag_list,
        created_at=db_article.created_at,
        updated_at=db_article.updated_at,
        author=author_profile,
    )

    return article_response


@router.get('/feed', response_model=MultArticle, status_code=200)
def get_feed(session: Session, current_user: CurrentUser):

    feed = session.scalars(
        select(Article)
        .where(
            Article.user_id == Follow.following_id,
            Follow.user_id == current_user.id,
        )
        .order_by(Article.created_at.desc())
    ).all()

    articles_list = []

    for article in feed:
        tags = []
        author_name = article.author
        tag_list = article.tag_list
        for tag in tag_list:
            tags.append(tag.tag_name)

        profile = Profile(
            username=author_name.username,
            bio=author_name.bio,
            image=author_name.image,
            email=author_name.email,
            following=True,
        )
        article_response: ArticleSchema = ArticleSchema(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tag_list=tags,
            created_at=article.created_at,
            updated_at=article.updated_at,
            author=profile,
        )
        articles_list.append(article_response)

    return {'articles': articles_list}


@router.get('/{slug}', response_model=ArticleSchema, status_code=200)
def get_article(slug: str, session: Session):

    article_user = session.scalar(select(Article).where(Article.slug == slug))

    following = False

    tags = []
    for tag in article_user.tag_list:
        tags.append(tag.tag_name)

    profile = Profile(
        username=article_user.author.username,
        bio=article_user.author.bio,
        image=article_user.author.image,
        email=article_user.author.email,
        following=following,
    )
    article_response: ArticleSchema = ArticleSchema(
        slug=article_user.slug,
        title=article_user.title,
        description=article_user.description,
        body=article_user.body,
        tag_list=tags,
        created_at=article_user.created_at,
        updated_at=article_user.updated_at,
        author=profile,
    )

    return article_response


@router.post('/{slug}/favorite', status_code=201)
def favorite_article(session: Session, current_user: CurrentUser, slug: str):
    article = session.scalar(select(Article).where(Article.slug == slug))
    if not article:
        raise HTTPException(status_code=404, detail='Article not exist')

    article_to_favorite = session.scalar(
        select(Favorites).where(
            Favorites.favorited_by_user == current_user.username,
            Favorites.article_slug == article.slug
        )
    )

    if article_to_favorite:
        raise HTTPException(
            status_code=400, detail='Article already favorited'
        )
    favorite: Favorites = Favorites(
        article_slug=slug, favorited_by_user=current_user.username
    )

    session.add(favorite)
    session.commit()
    session.refresh(favorite)

    # Return Article
    return {'favorite': favorite}


@router.delete('/{slug}/favorite', response_model=Message, status_code=201)
def unfavorite_article(session: Session, current_user: CurrentUser, slug: str):
    article = session.scalar(select(Article).where(Article.slug == slug))
    if not article:
        raise HTTPException(status_code=404, detail='Article not exist')

    article_to_unfavorite = session.scalar(
        select(Favorites).where(
            Favorites.favorited_by_user == current_user.username,
            Favorites.article_slug == article.slug
        )
    )
    if not article_to_unfavorite:
        raise HTTPException(
            status_code=400, detail='Article is not favorited'
        )

    session.delete(article_to_unfavorite)
    session.commit()

    # Return Article
    return {'detail': 'Unfavorited'}
