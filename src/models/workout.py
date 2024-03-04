from sqlalchemy.orm import relationship

from src.db.session import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class Workout(Base):
    """
    Workout table
    """
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    exercises = relationship("Exercise", back_populates="workout")


class Exercise(Base):
    """
    Exercise table
    """
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sets = Column(Integer)
    repetitions = Column(Integer)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    workout = relationship("Workout", back_populates="exercises")