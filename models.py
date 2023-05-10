from sqlalchemy import Column, Integer, String, Date, ForeignKey
from datetime import date

from sqlalchemy.orm import relationship

import db

Base = db.Base


class Users(Base):
    __tablename__ = 'MODULE_users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    fio = Column(String)
    marks = relationship("Marks", back_populates="student_rel")
    achievements = relationship("Achievements", back_populates="student_rel")


class Groups(Base):
    __tablename__ = 'MODULE_groups'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    description = Column(String, default='None')
    marks = relationship("Marks", back_populates="group_rel")


class Marks(Base):
    __tablename__ = 'MODULE_marks'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    student = Column(Integer, ForeignKey("MODULE_users.id"))
    group = Column(Integer, ForeignKey("MODULE_groups.id"))
    date = Column(Date, default=date.today())
    score = Column(Integer)

    student_rel = relationship("Users", back_populates="marks")
    group_rel = relationship("Groups", back_populates="marks")


class Achievements(Base):
    __tablename__ = 'MODULE_achievement'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    student = Column(Integer, ForeignKey("MODULE_users.id"))
    id_achievement = Column(Integer)
    description = Column(String)

    student_rel = relationship("Users", back_populates="achievements")
