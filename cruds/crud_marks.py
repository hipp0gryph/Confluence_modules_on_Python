from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, types
from typing import List

from sqlalchemy import func

from models import Marks, Users, Groups
from db import get_session

router = APIRouter()


class MarkIn(BaseModel):
    student: int
    group: int
    score: int


class MarkOut(BaseModel):
    id: int
    student: str
    group: str
    date: types.date
    score: int


class MarksWithName(BaseModel):
    student: str
    group: int
    scores: List[str]
    average_score: float
    rounded_score: int


@router.post('/marks', response_model=MarkOut, tags=['marks'])
def create_mark(mark: MarkIn):
    db_session = get_session()
    db_mark = Marks(student=mark.student, group=mark.group, score=mark.score)
    db_session.add(db_mark)
    db_session.commit()
    db_session.refresh(db_mark)
    mark_out = MarkOut(
        id=db_mark.id,
        student=db_mark.student,
        group=db_mark.group,
        date=db_mark.date,
        score=db_mark.score
    )
    return mark_out


@router.get('/marks', response_model=List[MarkOut], tags=['marks'])
def read_all_marks():
    db_session = get_session()
    db_mark = db_session.query(Marks).all()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    mark_out = []
    for mark in db_mark:
        mark_out.append(MarkOut(
            id=mark.id,
            student=mark.student,
            group=mark.group,
            date=mark.date,
            score=mark.score
        ))
    return mark_out


@router.get('/marks/{mark_id}', response_model=MarkOut, tags=['marks'])
def read_mark_by_id(mark_id: int):
    db_session = get_session()
    db_mark = db_session.query(Marks).filter(Marks.id == mark_id).first()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    mark_out = MarkOut(
        id=db_mark.id,
        student=db_mark.student,
        group=db_mark.group,
        date=db_mark.date,
        score=db_mark.score
    )
    return mark_out


@router.get('/marks/group/{group_id}', response_model=MarkOut, tags=['marks'])
def read_marks_by_group_id(group_id: int):
    db_session = get_session()
    db_mark = db_session.query(Marks).filter(Marks.group == group_id).all()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    mark_out = []
    for mark in db_mark:
        mark_out.append(MarkOut(
            id=mark.id,
            student=mark.student,
            group=mark.group,
            date=mark.date,
            score=mark.score
        ))
    return mark_out


@router.get('/read_marks_with_student_name', response_model=List[MarksWithName], tags=['marks'])
def read_marks_with_student_name():
    db_session = get_session()
    db_mark = db_session.query(
        Users.fio,
        Marks.group,
        func.array_agg(Marks.score),
        func.round(func.avg(Marks.score), 2).label('average_score'),
        func.round(func.avg(Marks.score)).label('rounded_score')
    ).join(
        Marks.student_rel
    ).join(
        Marks.group_rel
    ).group_by(
        Users.fio,
        Marks.group
    ).all()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    mark_out = []
    for mark in db_mark:
        mark_out.append(MarksWithName(
            student=mark[0],
            group=mark[1],
            scores=mark[2],
            average_score=mark[3],
            rounded_score=mark[4]
        ))
    return mark_out


@router.put('/marks/{mark_id}', response_model=MarkOut, tags=['marks'])
def update_mark(mark_id: int, mark: MarkIn):
    db_session = get_session()
    db_mark = db_session.query(Marks).filter(Marks.id == mark_id).first()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    db_mark.student = mark.student
    db_mark.group = mark.group
    db_mark.score = mark.score
    db_session.commit()
    db_session.refresh(db_mark)
    mark_out = MarkOut(
        id=db_mark.id,
        student=db_mark.student,
        group=db_mark.group,
        date=db_mark.date,
        score=db_mark.score
    )
    return mark_out


@router.delete('/marks/{mark_id}', response_model=MarkOut, tags=['marks'])
def delete_mark(mark_id: int):
    db_session = get_session()
    db_mark = db_session.query(Marks).filter(Marks.id == mark_id).first()
    if not db_mark:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='mark not found')
    mark_out = MarkOut(
        id=db_mark.id,
        student=db_mark.student,
        group=db_mark.group,
        date=db_mark.date,
        score=db_mark.score
    )
    db_session.expunge(db_mark)
    db_session.delete(db_mark)
    db_session.commit()
    return mark_out
