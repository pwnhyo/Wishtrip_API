import os
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from sqlalchemy.orm import Session
import models, schemas, db_api, database, authentication

import uvicorn
import logging
import shutil

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=database.engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login_for_access_token(form_data: schemas.LoginForm, db: Session = Depends(database.get_db)):
    db_user = db_api.get_user_by_username(db=db, username=form_data.username)

    if (not db_user) or (not authentication.verify_password(form_data.password, db_user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"username": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
def register(form_data: schemas.RegisterForm, db: Session = Depends(database.get_db)):
    username_exists = db_api.get_user_by_username(db=db, username=form_data.username)

    if username_exists:
        raise HTTPException(status_code=400, detail="username already registered")
    
    email_exists = db_api.get_user_by_email(db=db, email=form_data.email)
    if email_exists:
        raise HTTPException(status_code=400, detail="email already registered")

    user_register_success = db_api.create_user(db=db, form_data=form_data)
    #print(user_register_success.id)
    if user_register_success:
        return {"msg":"register success", "code":"200"}
    else:
        return HTTPException(status_code=400, detail="register error")


@app.post("/arpost/create")
def ar_post_create(arpost_name: str = Form(...), arpost_contents: str = Form(...), x_value: str = Form(...), y_value: str = Form(...), z_value: str = Form(...), file: Union[UploadFile, None] = None, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # db add
    arpost_create_success = db_api.create_arpost(db=db, username=username, arpost_name=arpost_name, arpost_contents=arpost_contents, x_value=x_value, y_value=y_value, z_value=z_value, updatetime=datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S'))

    # file write
    post_id = arpost_create_success.arpost_id
    for f in files:
        if ("." in f.filename or "/" in f.filename) and (f.filename.split(".")[-1] not in ['png', 'jpg']):
            continue
        with open(f"./uploads/arpost/{post_id}/{f.filename}", "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
    
    if arpost_create_success:
        return {"msg":"arpost create success", "code":200}
    else:
        return HTTPException(status_code=400, detail="arpost create error")


@app.post("/arpost/read")
def ar_post_read(arpost_id: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # db read
    db_post = db_api.read_arpost(db=db, arpost_id=arpost_id)
    if db_post:
        return db_post
    else:
        return {"msg":"No such arpost_id", "code":999}

@app.post("/arpost/edit")
def ar_post_update(arpost_id: int = Form(...), arpost_name: str = Form(...), arpost_contents: str = Form(...), x_value: str = Form(...), y_value: str = Form(...), z_value: str = Form(...), files: List[UploadFile] = File(description="Multiple files as UploadFile"), token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # check author permission
    db_post = db_api.read_arpost(db=db, arpost_id=arpost_id)
    if not db_post:
        return {"msg":"No such arpost_id", "code":999}
    if db_post.arpost_author != username:
        return {"msg":"You don't have permission", "code":999}

    # db edit
    arpost_edit_success = db_api.edit_arpost(db=db, username=username, arpost_name=arpost_name, arpost_contents=arpost_contents, x_value=x_value, y_value=y_value, z_value=z_value, updatetime=datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S'))

    # file write hmm..?
    post_id = arpost_create_success.arpost_id
    for f in files:
        if ("." in f.filename or "/" in f.filename) and (f.filename.split(".")[-1] not in ['png', 'jpg']):
            continue
        with open(f"./uploads/arpost/{post_id}/{f.filename}", "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
    
    if arpost_create_success:
        return {"msg":"arpost create success", "code":200}
    else:
        return HTTPException(status_code=400, detail="arpost create error")

    return username

@app.post("/arpost/delete")
def ar_post_delete(arpost_id: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # check author permission
    db_post = db_api.read_arpost(db=db, arpost_id=arpost_id)
    if not db_post:
        return {"msg":"No such arpost_id", "code":999}
    if db_post.arpost_author != username:
        return {"msg":"You don't have permission", "code":999}

    db_api.arpost_delete(db=db, arpost_id=arpost_id)
    return {"msg":"ARpost deleted success", "code":200}

@app.post("/arpost/get_around_posts")
def get_arround_posts(coordinates: schemas.ARpostCoordi, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

@app.post("/arpost/like/add")
def ar_post_like_add(arpost_like: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

@app.post("/arpost/like/delete")
def ar_post_like_delete(arpost_like: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

@app.post("/arpost/comment/add")
def ar_post_comment_add(arpost_comment: schemas.ARpostComment, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

@app.post("/arpost/comment/edit")
def ar_post_comment_edit(arpost_comment: schemas.ARpostCommentEdit, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

@app.post("/arpost/comment/delete")
def ar_post_comment_delete(arpost_comment: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    return username

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=9999, reload=True)