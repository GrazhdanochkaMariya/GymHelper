from sqlalchemy.orm import relationship

from src.db.session import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time


class Workout(Base):
    """
    Workout table
    """

    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    workout_date = Column(Date, nullable=True)
    workout_time = Column(Time, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")


class Exercise(Base):
    """
    Exercise table
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    sets = Column(Integer)
    repetitions = Column(Integer)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    workout = relationship("Workout", back_populates="exercises")
