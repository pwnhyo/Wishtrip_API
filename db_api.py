from sqlalchemy.orm import Session
import models
import schemas
import authentication
from typing import List, Union, Optional


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, form_data: schemas.RegisterForm):
    username = form_data.username
    name = form_data.name
    email = form_data.email
    hashed_password = authentication.get_password_hash(form_data.password)

    db_user = models.User(username=username, name=name,
                          email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_arpost(db: Session, username: str, arpost_name: str, arpost_contents: str, x_value: str, y_value: str, z_value: str, updatetime, image_filename, tag1: Optional[str], tag2: Optional[str], tag3: Optional[str], tag4: Optional[str], tag5: Optional[str], tag6: Optional[str], tag7: Optional[str], tag8: Optional[str], tag9: Optional[str], tag10: Optional[str]):
    db_arpost = models.ARpost(arpost_author=username, arpost_name=arpost_name, arpost_contents=arpost_contents, arpost_x_value=x_value, arpost_y_value=y_value, arpost_z_value=z_value, arpost_updatetime=updatetime,
                              arpost_image_filename=image_filename, arpost_tag1=tag1, arpost_tag2=tag2, arpost_tag3=tag3, arpost_tag4=tag4, arpost_tag5=tag5, arpost_tag6=tag6, arpost_tag7=tag7, arpost_tag8=tag8, arpost_tag9=tag9, arpost_tag10=tag10)
    db.add(db_arpost)
    db.commit()
    db.refresh(db_arpost)
    return db_arpost


def read_arpost(db: Session, arpost_id):
    return db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()


def edit_arpost(db: Session, arpost_id: int, username: str, arpost_name: str, arpost_contents: str, x_value: str, y_value: str, z_value: str, updatetime, image_filename, tag1: Optional[str], tag2: Optional[str], tag3: Optional[str], tag4: Optional[str], tag5: Optional[str], tag6: Optional[str], tag7: Optional[str], tag8: Optional[str], tag9: Optional[str], tag10: Optional[str]):
    db_arpost = db.query(models.ARpost).filter(
        models.ARpost.arpost_id == arpost_id).first()

    # edit
    db_arpost.arpost_author = username
    db_arpost.arpost_name = arpost_name
    db_arpost.arpost_contents = arpost_contents
    db_arpost.arpost_x_value = x_value
    db_arpost.arpost_y_value = y_value
    db_arpost.arpost_z_value = z_value
    db_arpost.arpost_image_filename = image_filename
    db_arpost.arpost_tag1 = tag1
    db_arpost.arpost_tag2 = tag2
    db_arpost.arpost_tag3 = tag3
    db_arpost.arpost_tag4 = tag4
    db_arpost.arpost_tag5 = tag5
    db_arpost.arpost_tag6 = tag6
    db_arpost.arpost_tag7 = tag7
    db_arpost.arpost_tag8 = tag8
    db_arpost.arpost_tag9 = tag9
    db_arpost.arpost_tag10 = tag10

    db.commit()
    db.refresh(db_arpost)
    return db_arpost


def delete_arpost(db: Session, arpost_id: int):
    db_arpost = db.query(models.ARpost).filter(
        models.ARpost.arpost_id == arpost_id).first()
    db.delete(db_arpost)
    db.commit()


def get_around_arposts(db: Session, x_value: str, y_value: str):
    return db.query(models.ARpost).all()


def add_emotion_arpost(db: Session, arpost_id: int, emotion: str, username: str):
    db_add_emotion = models.ARpost_emotion(
        arpost_id=arpost_id, emotion=emotion, username=username)
    db.add(db_add_emotion)
    db.commit()
    db.refresh(db_add_emotion)
    return db_add_emotion


def delete_emotion_arpost(db: Session, arpost_id: int, username: str):
    db_delete_emotion = db.query(models.ARpost_emotion).filter(
        models.ARpost_emotion.arpost_id == arpost_id).filter(models.ARpost_emotion.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()

def read_emotion_arpost(db: Session, arpost_id):
    return db.query(models.ARpost_emotion).filter(models.ARpost_emotion.arpost_id == arpost_id).all()


def exists_emotion_arpost(db: Session, arpost_id: int, username: str):
    return db.query(models.ARpost_emotion).filter(models.ARpost_emotion.arpost_id == arpost_id).filter(models.ARpost_emotion.username == username).first()



def add_comment_arpost(db: Session, arpost_id: int, comment: str, username: str, updatetime):
    db_add_comment = models.ARpost_comment(
        arpost_id=arpost_id, comment=comment, username=username, updatetime=updatetime)
    db.add(db_add_comment)
    db.commit()
    db.refresh(db_add_comment)
    return db_add_comment


def get_comment_arpost(db: Session, arpost_id: int, comment_id: int, username: str):
    return db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id == arpost_id).filter(models.ARpost_comment.comment_id == comment_id).filter(models.ARpost_comment.username == username).first()


def edit_comment_arpost(db: Session, arpost_id: int, comment_id: int, comment: str, username: str, updatetime):
    db_edit_comment = db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id == arpost_id).filter(
        models.ARpost_comment.comment_id == comment_id).filter(models.ARpost_comment.username == username).first()

    db_edit_comment.comment = comment
    db_edit_comment.updatetime = updatetime

    db.commit()
    db.refresh(db_edit_comment)
    return db_edit_comment


def delete_comment_arpost(db: Session, arpost_id: int, comment_id: int, username: str):
    db_delete_emotion = db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id == arpost_id).filter(
        models.ARpost_comment.comment_id == comment_id).filter(models.ARpost_comment.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()

def read_comment_arpost(db: Session, arpost_id):
    return db.query(models.ARpost_comment).filter(models.ARpost_comment.arpost_id == arpost_id).all()


def create_generalpost(db: Session, username: str, generalpost_name: str, generalpost_contents: str, updatetime, filenames, tag1: Optional[str], tag2: Optional[str], tag3: Optional[str], tag4: Optional[str], tag5: Optional[str], tag6: Optional[str], tag7: Optional[str], tag8: Optional[str], tag9: Optional[str], tag10: Optional[str]):
    db_generalpost = models.generalpost(generalpost_author=username, generalpost_name=generalpost_name, generalpost_contents=generalpost_contents, generalpost_updatetime=updatetime,
                              generalpost_image_filename1=filenames[0],
                              generalpost_image_filename2=filenames[1],
                              generalpost_image_filename3=filenames[2],
                              generalpost_image_filename4=filenames[3],
                              generalpost_image_filename5=filenames[4],
                              generalpost_image_filename6=filenames[5],
                              generalpost_image_filename7=filenames[6],
                              generalpost_image_filename8=filenames[7],
                              generalpost_image_filename9=filenames[8],
                              generalpost_image_filename10=filenames[9], generalpost_tag1=tag1, generalpost_tag2=tag2, generalpost_tag3=tag3, generalpost_tag4=tag4, generalpost_tag5=tag5, generalpost_tag6=tag6, generalpost_tag7=tag7, generalpost_tag8=tag8, generalpost_tag9=tag9, generalpost_tag10=tag10)
    db.add(db_generalpost)
    db.commit()
    db.refresh(db_generalpost)
    return db_generalpost

def read_generalpost(db: Session, generalpost_id):
    return db.query(models.generalpost).filter(models.generalpost.generalpost_id == generalpost_id).first()

def edit_generalpost(db: Session, username: str, generalpost_id: int, generalpost_name: str, generalpost_contents: str, updatetime, filenames, tag1: Optional[str], tag2: Optional[str], tag3: Optional[str], tag4: Optional[str], tag5: Optional[str], tag6: Optional[str], tag7: Optional[str], tag8: Optional[str], tag9: Optional[str], tag10: Optional[str]):
    db_generalpost = db.query(models.generalpost).filter(
        models.generalpost.generalpost_id == generalpost_id).first()
    
    db_generalpost.generalpost_author = username
    db_generalpost.generalpost_name = generalpost_name
    db_generalpost.generalpost_contents = generalpost_contents
    db_generalpost.generalpost_image_filename1 = filenames[0]
    db_generalpost.generalpost_image_filename2 = filenames[1]
    db_generalpost.generalpost_image_filename3 = filenames[2]
    db_generalpost.generalpost_image_filename4 = filenames[3]
    db_generalpost.generalpost_image_filename5 = filenames[4]
    db_generalpost.generalpost_image_filename6 = filenames[5]
    db_generalpost.generalpost_image_filename7 = filenames[6]
    db_generalpost.generalpost_image_filename8 = filenames[7]
    db_generalpost.generalpost_image_filename9 = filenames[8]
    db_generalpost.generalpost_image_filename10 = filenames[9]
    db_generalpost.generalpost_tag1 = tag1
    db_generalpost.generalpost_tag2 = tag2
    db_generalpost.generalpost_tag3 = tag3
    db_generalpost.generalpost_tag4 = tag4
    db_generalpost.generalpost_tag5 = tag5
    db_generalpost.generalpost_tag6 = tag6
    db_generalpost.generalpost_tag7 = tag7
    db_generalpost.generalpost_tag8 = tag8
    db_generalpost.generalpost_tag9 = tag9
    db_generalpost.generalpost_tag10 = tag10

    db.commit()
    db.refresh(db_generalpost)
    return db_generalpost

def delete_generalpost(db: Session, generalpost_id: int):
    db_generalpost = db.query(models.generalpost).filter(
        models.generalpost.generalpost_id == generalpost_id).first()
    db.delete(db_generalpost)
    db.commit()

def add_emotion_generalpost(db: Session, generalpost_id: int, emotion: str, username: str):
    db_add_emotion = models.generalpost_emotion(
        generalpost_id=generalpost_id, emotion=emotion, username=username)
    db.add(db_add_emotion)
    db.commit()
    db.refresh(db_add_emotion)
    return db_add_emotion


def delete_emotion_generalpost(db: Session, generalpost_id: int, username: str):
    db_delete_emotion = db.query(models.generalpost_emotion).filter(
        models.generalpost_emotion.generalpost_id == generalpost_id).filter(models.generalpost_emotion.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()

def read_emotion_generalpost(db: Session, generalpost_id):
    return db.query(models.generalpost_emotion).filter(models.generalpost_emotion.generalpost_id == generalpost_id).all()


def exists_emotion_generalpost(db: Session, generalpost_id: int, username: str):
    return db.query(models.generalpost_emotion).filter(models.generalpost_emotion.generalpost_id == generalpost_id).filter(models.generalpost_emotion.username == username).first()



def add_comment_generalpost(db: Session, generalpost_id: int, comment: str, username: str, updatetime):
    db_add_comment = models.generalpost_comment(
        generalpost_id=generalpost_id, comment=comment, username=username, updatetime=updatetime)
    db.add(db_add_comment)
    db.commit()
    db.refresh(db_add_comment)
    return db_add_comment


def get_comment_generalpost(db: Session, generalpost_id: int, comment_id: int, username: str):
    return db.query(models.generalpost_comment).filter(models.generalpost_comment.generalpost_id == generalpost_id).filter(models.generalpost_comment.comment_id == comment_id).filter(models.generalpost_comment.username == username).first()


def edit_comment_generalpost(db: Session, generalpost_id: int, comment_id: int, comment: str, username: str, updatetime):
    db_edit_comment = db.query(models.generalpost_comment).filter(models.generalpost_comment.generalpost_id == generalpost_id).filter(
        models.generalpost_comment.comment_id == comment_id).filter(models.generalpost_comment.username == username).first()

    db_edit_comment.comment = comment
    db_edit_comment.updatetime = updatetime

    db.commit()
    db.refresh(db_edit_comment)
    return db_edit_comment


def delete_comment_generalpost(db: Session, generalpost_id: int, comment_id: int, username: str):
    db_delete_emotion = db.query(models.generalpost_comment).filter(models.generalpost_comment.generalpost_id == generalpost_id).filter(
        models.generalpost_comment.comment_id == comment_id).filter(models.generalpost_comment.username == username).first()
    db.delete(db_delete_emotion)
    db.commit()


def read_comment_generalpost(db: Session, generalpost_id):
    return db.query(models.generalpost_comment).filter(models.generalpost_comment.generalpost_id == generalpost_id).all()

def exists_emotion_generalpost(db: Session, generalpost_id: int, username: str):
    return db.query(models.generalpost_emotion).filter(models.generalpost_emotion.generalpost_id == generalpost_id).filter(models.generalpost_emotion.username == username).first()