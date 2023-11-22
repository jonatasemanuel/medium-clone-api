from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Article, Comment, PostComment
from api.db.schemas import CommentSchema  # Message,
from api.routes.user import CurrentUser

router = APIRouter(prefix='/api/articles', tags=['Comments'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/{article_slug}/comments', status_code=201)
def post_comment(
    article_slug: str,
    body: CommentSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_article = session.scalar(
        select(Article).where(Article.slug == article_slug)
    )
    if db_article is None:
        raise HTTPException(status_code=404, detail='Article not found')

    comment: Comment = Comment(
        body=body.body,
        created_at=func.now(),
        updated_at=func.now(),
        author=current_user,
    )
    session.add(comment)
    session.commit()

    post_comment: PostComment = PostComment(
        article_slug=article_slug,
        comment_id=comment.id,
    )

    session.add(post_comment)
    session.commit()

    return {'comment': comment.body}


@router.get('/{slug}/comments', status_code=200)
def get_comments(slug: str, session: Session, current_user: CurrentUser):
    db_article = session.scalar(select(Article).where(Article.slug == slug))
    if db_article is None:
        raise HTTPException(status_code=404, detail='Article not found')

    comments_article = session.scalars(
        select(Comment).where(
            Comment.id == PostComment.comment_id,
            PostComment.article_slug == slug,
        )
    ).all()

    return {'comments': comments_article}


@router.delete('/{slug}/comments/{id}', status_code=200)
def delete_comment(
    slug: str, id: int, session: Session, current_user: CurrentUser
):
    db_article = session.scalar(select(Article).where(Article.slug == slug))
    if db_article is None:
        raise HTTPException(status_code=404, detail='Article not found')

    comment_association = session.scalar(
        select(PostComment).where(PostComment.comment_id == id)
    )
    session.delete(comment_association)

    comment_article = session.scalar(select(Comment).where(Comment.id == id))

    session.delete(comment_article)
    session.commit()

    return {'detail': 'Comment removed'}
