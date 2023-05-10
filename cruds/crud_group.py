from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import sqlalchemy

from models import Groups
from db import get_session

router = APIRouter()


class GroupIn(BaseModel):
    name: str
    description: str


class GroupOut(BaseModel):
    id: int
    name: str
    description: str


@router.post('/groups', response_model=GroupOut, tags=['groups'])
def create_group(group: GroupIn):
    db_session = get_session()
    db_group = Groups(name=group.name, description=group.description)
    db_session.add(db_group)
    db_session.commit()
    db_session.refresh(db_group)
    group_out = GroupOut(
        id=db_group.id,
        name=db_group.name,
        description=db_group.description
    )
    return group_out


@router.get('/groups', response_model=List[GroupOut], tags=['groups'])
def read_all_groups():
    db_session = get_session()
    db_groups = db_session.query(Groups).all()
    if not db_groups:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='groups not found')
    groups_out = []
    for db_group in db_groups:
        group_out = GroupOut(
            id=db_group.id,
            name=db_group.name,
            description=db_group.description
        )
        groups_out.append(group_out)
    return groups_out


@router.get('/groups/{group_id}', response_model=GroupOut, tags=['groups'])
def read_group_by_id(group_id: int):
    db_session = get_session()
    db_group = db_session.query(Groups).filter(Groups.id == group_id).first()
    if not db_group:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='group not found')
    group_out = GroupOut(
        id=db_group.id,
        name=db_group.name,
        description=db_group.description
    )
    return group_out


@router.put('/groups/{group_id}', response_model=GroupOut, tags=['groups'])
def update_group(group_id: int, group: GroupIn):
    db_session = get_session()
    db_group = db_session.query(Groups).filter(Groups.id == group_id).first()
    if not db_group:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='group not found')
    db_group.name = group.name
    db_group.description = group.description
    db_session.commit()
    db_session.refresh(db_group)
    group_out = GroupOut(
        id=db_group.id,
        name=db_group.name,
        description=db_group.description
    )
    return group_out


@router.delete('/groups/{group_id}', response_model=GroupOut, tags=['groups'])
def delete_group(group_id: int):
    db_session = get_session()
    db_group = db_session.query(Groups).filter(Groups.id == group_id).first()
    if not db_group:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='group not found')
    group_out = GroupOut(
        id=db_group.id,
        name=db_group.name,
        description=db_group.description
    )
    db_session.expunge(db_group)
    db_session.delete(db_group)
    db_session.commit()
    return group_out
