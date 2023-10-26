from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.security import (
    get_current_user,
    get_current_user_optional,
    get_password_hash
)
from api.db.database import get_session
from api.db.models import Follow, User
from api.db.schemas import (
    Profile,
    UserPrivate,
    UserSchema,
    Message,
    UserPublic,
    UserList,
    UserUpdate
)


router = APIRouter(prefix="/api", tags=["users"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/users", response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(
        User.username == user.username))

    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username.lower(),
        bio=user.bio,
        image=user.image,
        password=hashed_password,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/user", response_model=UserPrivate, status_code=200)
def get_user(
    current_user: CurrentUser,
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
):

    response = UserPrivate(
        token=token,
        username=current_user.username,
        bio=current_user.bio,
        image=current_user.image,
        email=current_user.email,
    )

    return response


@router.get("/profiles/{username}", response_model=Profile, status_code=200)
def get_profile(
    username: str,
    session: Session,
    current_user: Optional[User] = Depends(get_current_user_optional)
):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    following = False
    user_to_check = None

    if current_user:
        user_to_check = session.scalar(select(Follow).where(
            Follow.following_id == user.id, Follow.user_id == current_user.id))

    if user_to_check:
        following = True

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=following
    )
    return profile


@ router.post("/profiles/{username}/follow",
              response_model=Profile, status_code=201)
def follow_user(username: str, session: Session, current_user: CurrentUser):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not current_user:
        raise HTTPException(status_code=401, detail="User not logged in.")

    user_to_follow = session.scalar(select(Follow).where(
        Follow.following_id == user.id, Follow.user_id == current_user.id))
    if user_to_follow:
        raise HTTPException(status_code=400, detail="User already followed")

    follow = Follow(user_id=current_user.id, following_id=user.id)

    session.add(follow)
    session.commit()
    session.refresh(follow)

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=True
    )
    return profile


@ router.delete("/profiles/{username}/follow", response_model=Profile, status_code=201)
def unfollow_user(username: str, session: Session, current_user: CurrentUser):

    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not current_user:
        raise HTTPException(status_code=401, detail="User not logged in.")

    user_to_unfollow = session.scalar(select(Follow).where(
        Follow.following_id == user.id, Follow.user_id == current_user.id))
    if not user_to_unfollow:
        raise HTTPException(status_code=400, detail="User is not followed")

    session.delete(user_to_unfollow)
    session.commit()

    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image,
        email=user.email,
        following=False
    )
    return profile


@ router.get("/list", response_model=UserList, status_code=200)
def read_user(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@ router.put("/user", response_model=UserPublic)
def update_user(
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    """
    current_user.username = user.username
    current_user.password = user.password
    current_user.email = user.email
    current_user.bio = user.bio
    current_user.image = user.image
    """

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@ router.delete("/user", response_model=Message)
def delete_user(session: Session, current_user: CurrentUser):
    session.delete(current_user)
    session.commit()
    return {"detail": "User deleted"}
