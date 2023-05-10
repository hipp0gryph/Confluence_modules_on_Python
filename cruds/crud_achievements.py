from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import sqlalchemy
from sqlalchemy import func, Text

from models import Achievements, Users
from db import get_session

router = APIRouter()


class AchievementsIn(BaseModel):
    student: int
    id_achievement: int
    description: str


class AchievementsOut(BaseModel):
    id: int
    student: int
    id_achievement: int
    description: str


class AchievementsWithNames(BaseModel):
    student: str
    id_achievement: List[int]
    description: List[str]


@router.post('/achievements', response_model=AchievementsOut, tags=['achievements'])
def create_achievement(achievement: AchievementsIn):
    db_session = get_session()
    db_achievement = Achievements(student=achievement.student,
                                  id_achievement=achievement.id_achievement,
                                  description=achievement.description)
    db_session.add(db_achievement)
    db_session.commit()
    db_session.refresh(db_achievement)
    achievement_out = AchievementsOut(
        id=db_achievement.id,
        student=db_achievement.student,
        id_achievement=db_achievement.id_achievement,
        description=db_achievement.description
    )
    return achievement_out


@router.get('/achievements', response_model=List[AchievementsOut], tags=['achievements'])
def read_all_achievements():
    db_session = get_session()
    db_achievements = db_session.query(Achievements).all()
    if not db_achievements:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='achievements not found')
    achievements_out = []
    for db_achievement in db_achievements:
        achievement_out = AchievementsOut(
            id=db_achievement.id,
            student=db_achievement.student,
            id_achievement=db_achievement.id_achievement,
            description=db_achievement.description
        )
        achievements_out.append(achievement_out)
    return achievements_out


@router.get('/achievements/{achievement_id}', response_model=AchievementsOut, tags=['achievements'])
def read_achievement_by_id(achievement_id: int):
    db_session = get_session()
    db_achievement = db_session.query(Achievements).filter(Achievements.id == achievement_id).first()
    if not db_achievement:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='achievement not found')
    achievement_out = AchievementsOut(
        id=db_achievement.id,
        student=db_achievement.student,
        id_achievement=db_achievement.id_achievement,
        description=db_achievement.description
    )
    return achievement_out


@router.get('/achievements_with_names', response_model=List[AchievementsWithNames], tags=['achievements'])
def read_achievements_with_names():
    db_session = get_session()
    db_achievements = db_session.query(Users.fio,
                                       func.array_agg(Achievements.id_achievement),
                                       func.array_agg(Achievements.description))\
        .join(Achievements)\
        .group_by(Users.id)\
        .all()
    if not db_achievements:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='achievement not found')
    achievements_out = []
    for db_achievement in db_achievements:
        achievements_out.append(AchievementsWithNames(
            student=db_achievement[0],
            id_achievement=db_achievement[1],
            description=db_achievement[2]
        ))
    return achievements_out


@router.put('/achievements/{achievement_id}', response_model=AchievementsOut, tags=['achievements'])
def update_achievement(achievement_id: int, achievement: AchievementsIn):
    db_session = get_session()
    db_achievement = db_session.query(Achievements).filter(Achievements.id == achievement_id).first()
    if not db_achievement:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='achievement not found')
    db_achievement.student = achievement.student
    db_achievement.id_achievement = achievement.id_achievement
    db_achievement.description = achievement.description
    db_session.commit()
    db_session.refresh(db_achievement)
    achievement_out = AchievementsOut(
        id=db_achievement.id,
        student=db_achievement.student,
        id_achievement=db_achievement.id_achievement,
        description=db_achievement.description
    )
    return achievement_out


@router.delete('/achievements/{achievement_id}', response_model=AchievementsOut, tags=['achievements'])
def delete_achievement(achievement_id: int):
    db_session = get_session()
    db_achievement = db_session.query(Achievements).filter(Achievements.id == achievement_id).first()
    if not db_achievement:
        db_session.rollback()
        raise HTTPException(status_code=404, detail='achievement not found')
    achievement_out = AchievementsOut(
        id=db_achievement.id,
        student=db_achievement.student,
        id_achievement=db_achievement.id_achievement,
        description=db_achievement.description
    )
    return achievement_out
