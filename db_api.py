from sqlalchemy.orm import Session
import models,  schemas, authentication

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

    prnt(username, name, email, hashed_password)
    db_user = models.User(username=username, name=name, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_arpost(db: Session, username : str, arpost_name : str, arpost_contents : str, x_value : str, y_value : str, z_value : str, updatetime):
    db_arpost = models.ARpost(arpost_author=username, arpost_name=arpost_name, arpost_contents=arpost_contents, arpost_x_value=x_value, arpost_y_value=y_value, arpost_z_value=z_value, arpost_updatetime=updatetime)
    db.add(db_user)
    db.commit()
    db.refresh(db_arpost)
    return db_arpost

def read_arpost(db: Session, arpost_id):
    return  db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()

def edit_arpost(db: Session, arpost_id: int,  username : str, arpost_name : str, arpost_contents : str, x_value : str, y_value : str, z_value : str, updatetime):
    db_arpost = db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()
    
    # edit
    db_arpost.arpost_id = arpost_id
    db_arpost.arpost_author = username
    db_arpost.arpost_name = arpost_name
    db_arpost.arpost_contents = arpost_contents
    db_arpost.arpost_x_value = arpost_x_value
    db_arpost.arpost_y_value = arpost_y_value
    db_arpost.arpost_z_value = arpost_z_value
    db_arpost.arpost_updatetime = updatetime

    db.commit()
    db.refresh(db_arpost)
    return db_arpost

def update_arpost(db: Session):
    db_arpost = db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()
    # edit
    
    db.commit()
    db.refresh(db_arpost)
    return db_arpost

def arpost_delete(db: Session, arpost_id : int):
    db_arpost = db.query(models.ARpost).filter(models.ARpost.arpost_id == arpost_id).first()
    db.delete()
    db.commit()
