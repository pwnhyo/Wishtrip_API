from sqlalchemy.orm import Session
import models,  schemas, authentication
from typing import List, Union, Optional

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, form_data: schemas.RegisterForm):
    username=form_data.username
    name=form_data.name
    email=form_data.email
    hashed_password=authentication.get_password_hash(form_data.password)

    db_user = models.User(username=username, name=name, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_arpost(db: Session, username : str, arpost_name : str, arpost_contents : str, x_value : str, y_value : str, z_value : str, updatetime, image_filename, tag1: Union[str, None], tag2: Union[str, None], tag3: Union[str, None]):
    db_arpost = models.ARpost(arpost_author=username, arpost_name=arpost_name, arpost_contents=arpost_contents, arpost_x_value=x_value, arpost_y_value=y_value, arpost_z_value=z_value, arpost_updatetime=updatetime, arpost_image_filename=image_filename, arpost_tag1=tag1, arpost_tag2=tag2, arpost_tag3=tag3)
    db.add(db_arpost)
    db.commit()
    db.refresh(db_arpost)
    return db_arpost

def read_arpost(db: Session, arpost_id):
    return  db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()

def edit_arpost(db: Session, arpost_id: int,  username : str, arpost_name : str, arpost_contents : str, x_value : str, y_value : str, z_value : str, updatetime, image_filename, tag1: Union[str, None], tag2: Union[str, None], tag3: Union[str, None]):
    db_arpost = db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()

    # edit
    db_arpost.arpost_author = username
    db_arpost.arpost_name = arpost_name
    db_arpost.arpost_contents = arpost_contents
    db_arpost.arpost_x_value = x_value
    db_arpost.arpost_y_value = y_value
    db_arpost.arpost_z_value = z_value
    db_arpost.arpost_updatetime = updatetime
    db_arpost.arpost_image_filename = image_filename
    db_arpost.arpost_tag1 = tag1
    db_arpost.arpost_tag2 = tag2
    db_arpost.arpost_tag3 = tag3

    db.commit()
    db.refresh(db_arpost)
    return db_arpost

def delete_arpost(db: Session, arpost_id : int):
    db_arpost = db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()
    db.delete(db_arpost)
    db.commit()

def get_around_arposts(db: Session, x_value: str, y_value: str):
    return db.query(models.ARpost).all()

def add_emotion_arpost(db: Session, arpost_id: int, emotion: str, username: str):
    db_add_emotion = models.ARpost_emotion(arpost_id=arpost_id, emotion=emotion, username=username)
    db.add(db_add_emotion)
    db.commit()
    db.refresh(db_add_emotion)
    return db_add_emotion

def delete_emotion_arpost(db: Session, arpost_id: int, username: str):
    db_delete_emotion = db.query(models.ARpost_emotion).filter(models.ARpost_emotion.arpost_id == arpost_id).filter(models.ARpost_emotion.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()

def exists_emotion_arpost(db: Session, arpost_id: int, username: str):
    return db.query(models.ARpost_emotion).filter(models.ARpost_emotion.arpost_id==arpost_id).filter(models.ARpost_emotion.username==username).first()

def add_comment_arpost(db: Session, arpost_id: int, comment: str, username: str):
    db_add_comment = models.ARpost_comment(arpost_id=arpost_id, comment=comment, username=username)
    db.add(db_add_comment)
    db.commit()
    db.refresh(db_add_comment)
    return db_add_comment

def get_comment_arpost(db: Session, arpost_id: int, comment_id: int, username: str):
    return db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id==arpost_id).filter(models.ARpost_comment.comment_id==comment_id).filter(models.ARpost_comment.username==username).first()

def edit_comment_arpost(db: Session, arpost_id: int, comment_id: int, comment: str, username: str):
    db_edit_comment = db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id==arpost_id).filter(models.ARpost_comment.comment_id==comment_id).filter(models.ARpost_comment.username==username).first()

    db_edit_comment.comment = comment

    db.commit()
    db.refresh(db_edit_comment)
    return db_edit_comment

def delete_comment_arpost(db: Session, arpost_id: int, comment_id: int, username: str):
    db_delete_emotion = db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id == arpost_id).filter(models.ARpost_comment.comment_id==comment_id).filter(models.ARpost_comment.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()