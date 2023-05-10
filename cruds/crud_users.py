from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import sqlalchemy

from models import Users
from db import get_session

router = APIRouter()


class UserIn(BaseModel):
    fio: str


class UserOut(BaseModel):
    id: int
    fio: str


@router.post('/users', response_model=UserOut, tags=['users'])
def create_user(user: UserIn):
    db_session = get_session()
    db_user = Users(fio=user.fio)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    user_out = UserOut(
        id=db_user.id,
        fio=db_user.fio
    )
    return user_out


@router.get('/users', response_model=List[UserOut], tags=['users'])
def read_all_users():
    db_session = get_session()
    db_user = db_session.query(Users).all()
    if not db_user:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='user not found')
    user_out = []
    for user in db_user:
        user_out.append(UserOut(
            id=user.id,
            fio=user.fio
        ))
    return user_out


@router.get('/users/{user_id}', response_model=UserOut, tags=['users'])
def read_user_by_id(user_id: int):
    db_session = get_session()
    db_user = db_session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='user not found')
    user_out = UserOut(
        id=db_user.id,
        fio=db_user.fio
    )
    return user_out


@router.put('/users/{user_id}', response_model=UserOut, tags=['users'])
def update_user(user_id: int, user: UserIn):
    db_session = get_session()
    db_user = db_session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='user not found')
    db_user.fio = user.fio
    db_session.commit()
    db_session.refresh(db_user)
    user_out = UserOut(
        id=db_user.id,
        fio=db_user.fio
    )
    return user_out


@router.delete('/users/{user_id}', response_model=UserOut, tags=['users'])
def delete_user(user_id: int):
    db_session = get_session()
    db_user = db_session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='user not found')
    user_out = UserOut(
        id=db_user.id,
        fio=db_user.fio
    )
    db_session.expunge(db_user)
    db_session.delete(db_user)
    db_session.commit()
    return user_out
