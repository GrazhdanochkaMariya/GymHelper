from datetime import datetime

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from enum import Enum as EnumType

from src.db.session import Base
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Float


class TypeEnum(str, EnumType):
    """Str enum for score level type"""

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    MASTER = "MASTER"


class User(Base):
    """
    User table
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=True)
    age = Column(BigInteger, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)
    score = Column(BigInteger, nullable=True)
    score_level = Column(ENUM(TypeEnum), default=TypeEnum.BEGINNER)
    avatar_path = Column(String, nullable=True)

    measurements = relationship("UserMeasurements", back_populates="user")
    workouts = relationship("Workout", back_populates="user")


class UserMeasurements(Base):
    """
    User measurements table
    """

    __tablename__ = "user_measurements"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    biceps = Column(Float, nullable=True)
    waist = Column(Float, nullable=True)
    hips = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="measurements")
