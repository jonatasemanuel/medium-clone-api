from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import Follow, User
from api.db.schemas import Message, Profile
from api.security import get_current_user, get_current_user_optional

router = APIRouter(prefix='/api/profiles', tags=['Profile'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/{username}', response_model=Profile, status_code=200)
def get_profile(
    username: str,
    session: Session,
    current_user: Optional[User] = Depends(get_current_user_optional),
):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    following = False
    user_to_check = None

    if current_user:
        user_to_check = session.scalar(
            select(Follow).where(
                Follow.following_id == user.id,
                Follow.user_id == current_user.id,
            )
        )

    if user_to_check:
        following = True

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=following,
    )
    return profile


@router.post('/{username}/follow', response_model=Profile, status_code=201)
def follow_user(username: str, session: Session, current_user: CurrentUser):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not current_user:
        raise HTTPException(status_code=401, detail='User not logged in.')

    user_to_follow = session.scalar(
        select(Follow).where(
            Follow.following_id == user.id, Follow.user_id == current_user.id
        )
    )
    if user_to_follow:
        raise HTTPException(status_code=400, detail='User already followed')

    follow = Follow(user_id=current_user.id, following_id=user.id)

    session.add(follow)
    session.commit()
    session.refresh(follow)

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=True,
    )
    return profile


@router.delete('/{username}/follow', response_model=Profile, status_code=201)
def unfollow_user(username: str, session: Session, current_user: CurrentUser):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not current_user:
        raise HTTPException(status_code=401, detail='User not logged in.')

    user_to_unfollow = session.scalar(
        select(Follow).where(
            Follow.following_id == user.id, Follow.user_id == current_user.id
        )
    )
    if not user_to_unfollow:
        raise HTTPException(status_code=400, detail='User is not followed')

    session.delete(user_to_unfollow)
    session.commit()

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=False,
    )
    return profile
