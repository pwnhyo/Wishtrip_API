from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import timedelta, datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    name = Column(String(32))
    email = Column(String, unique=True)
    hashed_password = Column(String)

class ARpost(Base):
    __tablename__ = "arposts"

    arpost_id = Column(Integer, primary_key=True, index=True)
    arpost_author = Column(String(32), index=True)
    arpost_name = Column(String(512))
    arpost_contents = Column(String(8192))
    arpost_x_value = Column(String(64))
    arpost_y_value = Column(String(64))
    arpost_z_value = Column(String(64))
    arpost_updatetime = Column(DateTime)