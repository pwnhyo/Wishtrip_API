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
    updatetime = Column(DateTime)

class generalpost(Base):
    __tablename__ = "generalposts"

    generalpost_id = Column(Integer, primary_key=True, index=True)
    generalpost_author = Column(String(32), index=True)
    generalpost_name = Column(String(512))
    generalpost_contents = Column(String(8192))
    generalpost_updatetime = Column(DateTime)
    generalpost_image_filename1 = Column(String(256))
    generalpost_image_filename2 = Column(String(256))
    generalpost_image_filename3 = Column(String(256))
    generalpost_image_filename4 = Column(String(256))
    generalpost_image_filename5 = Column(String(256))
    generalpost_image_filename6 = Column(String(256))
    generalpost_image_filename7 = Column(String(256))
    generalpost_image_filename8 = Column(String(256))
    generalpost_image_filename9 = Column(String(256))
    generalpost_image_filename10 = Column(String(256))
    generalpost_tag1 = Column(String(128))
    generalpost_tag2 = Column(String(128))
    generalpost_tag3 = Column(String(128))
    generalpost_tag4 = Column(String(128))
    generalpost_tag5 = Column(String(128))
    generalpost_tag6 = Column(String(128))
    generalpost_tag7 = Column(String(128))
    generalpost_tag8 = Column(String(128))
    generalpost_tag9 = Column(String(128))
    generalpost_tag10 = Column(String(128))

class generalpost_emotion(Base):
    __tablename__ = "generalpost_emotion"

    emotion_id = Column(Integer, primary_key=True, index=True)
    generalpost_id  = Column(Integer, ForeignKey('generalposts.generalpost_id'))
    emotion = Column(String(128))
    username = Column(String(512))


class generalpost_comment(Base):
    __tablename__ = "generalpost_comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    generalpost_id  = Column(Integer, ForeignKey('generalposts.generalpost_id'))
    comment = Column(String(512))
    username = Column(String(512))
    updatetime = Column(DateTime)