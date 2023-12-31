from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import TagArticle

router = APIRouter(prefix='/api/tags', tags=['Tags'])
Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=200)
def get_tags(
    session: Session, offset: Optional[int] = 0, limit: Optional[int] = 20
):
    db_tags = session.scalars(select(TagArticle.tag_name)).all()
    tags = set(db_tags)
    return {'tags': tags}
