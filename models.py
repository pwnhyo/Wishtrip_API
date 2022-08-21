from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship, backref
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
    arpost_image_filename = Column(String(128))
    arpost_tag1 = Column(String(128))
    arpost_tag2 = Column(String(128))
    arpost_tag3 = Column(String(128))
    arpost_tag4 = Column(String(128))
    arpost_tag5 = Column(String(128))
    arpost_tag6 = Column(String(128))
    arpost_tag7 = Column(String(128))
    arpost_tag8 = Column(String(128))
    arpost_tag9 = Column(String(128))
    arpost_tag10 = Column(String(128))

class ARpost_emotion(Base):
    __tablename__ = "arpost_emotion"

    emotion_id = Column(Integer, primary_key=True, index=True)
    arpost_id  = Column(Integer, ForeignKey('arposts.arpost_id'))
    emotion = Column(String(128))
    username = Column(String(512))


class ARpost_comment(Base):
    __tablename__ = "arpost_comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    arpost_id  = Column(Integer, ForeignKey('arposts.arpost_id'))
    comment = Column(String(512))
    username = Column(String(512))

