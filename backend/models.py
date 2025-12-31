from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    games = relationship("Games", back_populates='user', cascade='all, delete')

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'))
    user_name = Column(ForeignKey('users.username'))

    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    date = Column(String, nullable=False)

    user = relationship('Users', back_populates='games')