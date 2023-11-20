from typing import Optional, Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.models import Tag, TagArticle
from api.db.database import get_session

router = APIRouter(prefix='/api/tags', tags=['tags'])
Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=200)
def get_tags(
    session: Session,
    offset: Optional[int] = 0,
    limit: Optional[int] = 20
):
    db_tags = session.scalars(select(Tag.name)).all()
    tags = set(db_tags)
    return {'tags': tags}
