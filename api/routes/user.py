from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import User
from api.db.schemas import (
    Message,
    Token,
    UserList,
    UserPrivate,
    UserPublic,
    UserSchema,
    UserUpdate,
)
from api.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix='/api', tags=['User and Authentication'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/users/login', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}


@router.post('/users', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

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


@router.get('/user', response_model=UserPrivate, status_code=200)
def get_user(
    current_user: CurrentUser,
    token: str = Depends(OAuth2PasswordBearer(tokenUrl='token')),
):

    response = UserPrivate(
        token=token,
        username=current_user.username,
        bio=current_user.bio,
        image=current_user.image,
        email=current_user.email,
    )

    return response


@router.get('/user/list', response_model=UserList, status_code=200)
def read_user(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/user', response_model=UserPublic)
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


@router.delete('/user', response_model=Message)
def delete_user(session: Session, current_user: CurrentUser):
    session.delete(current_user)
    session.commit()
    return {'detail': 'User deleted'}
