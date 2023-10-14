from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from api.db.database import get_session
from api.db.models import Tag


Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/tag', tags=['tags'])


@router.post('/', response_model=Tag)
def create_tag(tag: Tag, session: Session):

    db_tag = Tag(
        slug=tag.slug
    )

    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
