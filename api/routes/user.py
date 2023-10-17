from sqlalchemy import select

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.db.database import get_session
from api.db.models import User
from api.db.schemas import UserAuthenticated, UserSchema, Message, UserPublic, UserList
from api.security import get_current_user, get_password_hash


router = APIRouter(prefix='/api', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/users', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail='Username already registered'
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username.lower(),
        bio=user.bio,
        image=user.image,
        password=hashed_password,
        email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/user/{user_id}', response_model=UserPublic, status_code=200)
def get_user(
    user_id: int,
    current_user: CurrentUser,
):
    """
    To do:

    [ ] - Switch response model to authentication scheme
    [ ] - Remove id parameter, use just current user
    """

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    return current_user


@router.get('/profiles/{username}', response_model=UserPublic, status_code=200)
def get_profile(username: str, session: Session):
    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user


@router.get('/list', response_model=UserList, status_code=200)
def read_user(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/user/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    """
    Atualizar para patch e  mudar Schema -> não utilizar id de busca
    Não precisa confirmar usuario pois esta confirmando no current_user?
    """

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = user.password
    current_user.email = user.email
    current_user.bio = user.bio
    current_user.image = user.image

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()
    return {'detail': 'User deleted'}
