from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Tag
from api.db.schemas import TagSchema


Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/api/tag', tags=['tags'])


@router.post('/', response_model=TagSchema, status_code=201)
def create_tag(tag: TagSchema, session: Session):

    db_tag = Tag(
        slug=tag.slug
    )

    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)

    return db_tag
