from datetime import datetime

from sqlalchemy.orm import relationship

from src.db.session import Base
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Float


class User(Base):
    """
    User table
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    measurements = relationship("UserMeasurements", back_populates="user")


class UserMeasurements(Base):
    """
    User measurements table
    """

    __tablename__ = "user_measurements"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    biceps = Column(Float, nullable=False)
    waist = Column(Float, nullable=False)
    hips = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="measurements")
