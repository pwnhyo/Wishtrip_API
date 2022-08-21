import os
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from sqlalchemy.orm import Session
import models, schemas, db_api, database, authentication
from starlette.responses import StreamingResponse

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
            detail="Incorrect username or password.",
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
        raise HTTPException(status_code=400, detail="username already registered.")
    
    email_exists = db_api.get_user_by_email(db=db, email=form_data.email)
    if email_exists:
        raise HTTPException(status_code=400, detail="email already registered.")

    user_register_success = db_api.create_user(db=db, form_data=form_data)
    #print(user_register_success.id)
    if user_register_success:
        return {"detail":"register success."}
    else:
        raise HTTPException(status_code=400, detail="register error.")


@app.post("/arpost/create")
def ar_post_create(arpost_name: str = Form(...), arpost_contents: str = Form(...), x_value: str = Form(...), y_value: str = Form(...), z_value: str = Form(...), tag1 : Optional[str] = Form(None), tag2 : Optional[str] = Form(None), tag3: Optional[str] = Form(None), file: Union[UploadFile, None] = None, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # db add
    arpost_create_success = db_api.create_arpost(db=db, username=username, arpost_name=arpost_name, arpost_contents=arpost_contents, x_value=x_value, y_value=y_value, z_value=z_value, updatetime=datetime.now(), image_filename=file.filename, tag1=tag1, tag2=tag2, tag3=tag3)
    
    # file save
    if (".." in file.filename or "/" in file.filename) or (file.filename.split(".")[-1] not in ['png', 'jpg']):
        db_api.delete_arpost(db=db, arpost_id=arpost_create_success.arpost_id)
        raise HTTPException(status_code=400, detail="Not allowed file.")

    if not os.path.exists(f"./uploads"):
        os.makedirs(f"./uploads")

    if not os.path.exists(f"./uploads/arpost"):
        os.makedirs(f"./uploads/arpost")

    if not os.path.exists(f"./uploads/arpost/{arpost_create_success.arpost_id}"):
        os.makedirs(f"./uploads/arpost/{arpost_create_success.arpost_id}")

    open(f"./uploads/arpost/{arpost_create_success.arpost_id}/{file.filename}", "wb").write(file.file.read())

    # return
    if arpost_create_success:
        return {"detail":"arpost create success", "arpost_id":arpost_create_success.arpost_id}
    else:
        raise HTTPException(status_code=400, detail="create arpost error.")

@app.post("/arpost/read")
def ar_post_read(read_form: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # db read
    db_post = db_api.read_arpost(db=db, arpost_id=read_form.arpost_id)
    if db_post:
        return_parse = {'arpost_id':db_post.arpost_id, 'arpost_author':db_post.arpost_author, 'arpost_name':db_post.arpost_name, 'arpost_contents':db_post.arpost_contents, 'arpost_image_url':f'/arpost_image_view?arpost_id={db_post.arpost_id}&arpost_image_filename={db_post.arpost_image_filename}', 'arpost_x_value':db_post.arpost_x_value, 'arpost_y_value':db_post.arpost_y_value, 'arpost_z_value':db_post.arpost_z_value, 'arpost_updatetime':db_post.arpost_updatetime, 'arpost_tag1':db_post.arpost_tag1, 'arpost_tag2':db_post.arpost_tag2, 'arpost_tag3':db_post.arpost_tag3}
        return return_parse
    else:
        raise HTTPException(status_code=400, detail="No such arpost_id.")

@app.get("/arpost_image_view")
def arpost_image_view(arpost_id: int, arpost_image_filename: str):
    try:
        if (".." in arpost_image_filename or "/" in arpost_image_filename) or (arpost_image_filename.split(".")[-1] not in ['png', 'jpg']):
            raise
        image_bytes = open(f"./uploads/arpost/{arpost_id}/{arpost_image_filename}", "rb").read()
    except:
        return Response(content="", media_type="image/png")
    return Response(content=image_bytes, media_type="image/png")

@app.post("/arpost/edit")
def ar_post_update(arpost_id: int = Form(...), arpost_name: str = Form(...), arpost_contents: str = Form(...), x_value: str = Form(...), y_value: str = Form(...), z_value: str = Form(...), tag1 : Optional[str] = Form(None), tag2 : Optional[str] = Form(None), tag3: Optional[str] = Form(None), file: Union[UploadFile, None] = None, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # check author permission
    db_post = db_api.read_arpost(db=db, arpost_id=arpost_id)
    if not db_post:
        raise HTTPException(status_code=400, detail="No such arpost_id.")
    if db_post.arpost_author != username:
        raise HTTPException(status_code=400, detail="You don't have permission.")

    # db edit
    arpost_edit_success = db_api.edit_arpost(db=db, username=username, arpost_id=arpost_id, arpost_name=arpost_name, arpost_contents=arpost_contents, x_value=x_value, y_value=y_value, z_value=z_value, updatetime=datetime.now(), image_filename=file.filename, tag1=tag1, tag2=tag2, tag3=tag3)

    # file save
    if (".." in file.filename or "/" in file.filename) or (file.filename.split(".")[-1] not in ['png', 'jpg']):
        raise HTTPException(status_code=400, detail="Not allowed file.")

    if not os.path.exists(f"./uploads/arpost/{arpost_edit_success.arpost_id}"):
        os.makedirs(f"./uploads/arpost/{arpost_edit_success.arpost_id}")

    open(f"./uploads/arpost/{arpost_edit_success.arpost_id}/{file.filename}", "wb").write(file.file.read())
    
    # return
    if arpost_edit_success:
        return {"detail":"edit arpost success.", "arpost_id":arpost_edit_success.arpost_id}
    else:
        raise HTTPException(status_code=400, detail="edit arpost error.")

    return username

@app.post("/arpost/delete")
def ar_post_delete(delete_form: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # check login
    username = authentication.check_credentials(token)

    # check author permission
    db_post = db_api.read_arpost(db=db, arpost_id=delete_form.arpost_id)
    if not db_post:
        raise HTTPException(status_code=400, detail="No such arpost_id.")
    if db_post.arpost_author != username:
        raise HTTPException(status_code=400, detail="You don't have permission.")

    db_api.delete_arpost(db=db, arpost_id=delete_form.arpost_id)
    return {"detail":"delete arpost success."}

@app.post("/arpost/get_around_posts")
def get_arround_posts(coordinates: schemas.ARpostCoordi, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    db_around_posts = db_api.get_around_arposts(db=db, x_value=coordinates.x_value, y_value=coordinates.y_value)
    
    if not db_around_posts:
        raise HTTPException(status_code=400, detail="There are no AR posts around.")

    return_array = []
    for db_post in db_around_posts:
        return_parse = {'arpost_id':db_post.arpost_id, 'arpost_author':db_post.arpost_author, 'arpost_name':db_post.arpost_name, 'arpost_contents':db_post.arpost_contents, 'arpost_image_url':f'/arpost_image_view?arpost_id={db_post.arpost_id}&arpost_image_filename={db_post.arpost_image_filename}', 'arpost_x_value':db_post.arpost_x_value, 'arpost_y_value':db_post.arpost_y_value, 'arpost_z_value':db_post.arpost_z_value, 'arpost_updatetime':db_post.arpost_updatetime, 'arpost_tag1':db_post.arpost_tag1, 'arpost_tag2':db_post.arpost_tag2, 'arpost_tag3':db_post.arpost_tag3}
        return_array.append(return_parse)

    return return_array

@app.post("/arpost/emotion/add")
def ar_post_like_add(emotion_form: schemas.ARpostEmotion, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # check arpost_id
    check_arpost_id = db_api.read_arpost(db=db, arpost_id=emotion_form.arpost_id)
    if not check_arpost_id:
        raise HTTPException(status_code=400, detail="Not exists arpost_id.")

    # check emoji
    if not (emotion_form.emotion in [':슬픔:', ':놀람:', ':웃김:', ':따봉:', ':하트:']):
        raise HTTPException(status_code=400, detail="Not allowed emoji.")

    # check duplication
    check_emotion_duplication = db_api.exists_emotion_arpost(db=db, arpost_id=emotion_form.arpost_id, username=username)
    if check_emotion_duplication:
        raise HTTPException(status_code=400, detail="arpost emotion duplication.")
    
    # add emotion
    add_emotion_success = db_api.add_emotion_arpost(db=db, arpost_id=emotion_form.arpost_id, emotion=emotion_form.emotion, username=username)

    # return
    if add_emotion_success:
        return {"detail":"add arpost_emotion success","arpost_id":add_emotion_success.arpost_id}
    else:
        raise HTTPException(status_code=400, detail="add arpost_emotion error.")

@app.post("/arpost/emotion/delete")
def ar_post_like_delete(emotion_form: schemas.ARpostId, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # check arpost_id
    check_arpost_id = db_api.read_arpost(db=db, arpost_id=emotion_form.arpost_id)
    if not check_arpost_id:
        raise HTTPException(status_code=400, detail="Not exists arpost_id.")

    # check emotion exist
    check_emotion_duplication = db_api.exists_emotion_arpost(db=db, arpost_id=emotion_form.arpost_id, username=username)
    if not check_emotion_duplication:
        raise HTTPException(status_code=400, detail="Emotion does not exist.")

    # delete emotion
    db_api.delete_emotion_arpost(db=db, arpost_id=emotion_form.arpost_id, username=username)
    
    return {"detail":"delete arpost_emotion success","arpost_id":emotion_form.arpost_id}


@app.post("/arpost/comment/add")
def ar_post_comment_add(comment_form: schemas.ARpostComment, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # check arpost_id
    check_arpost_id = db_api.read_arpost(db=db, arpost_id=comment_form.arpost_id)
    if not check_arpost_id:
        raise HTTPException(status_code=400, detail="Not exists arpost_id.")

    # length check
    if len(comment_form.comment) > 512:
        raise HTTPException(status_code=400, detail="comment length < 512.")

    # add comment
    add_comment_success = db_api.add_comment_arpost(db=db, arpost_id=comment_form.arpost_id, comment=comment_form.comment, username=username)

    # return
    if add_comment_success:
        return {"detail":"add arpost_comment success.","arpost_id":add_comment_success.arpost_id}
    else:
        raise HTTPException(status_code=400, detail="add arpost_comment error.")

@app.post("/arpost/comment/edit")
def ar_post_comment_edit(comment_edit_form: schemas.ARpostCommentEdit, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)

    # check arpost_id
    check_arpost_id = db_api.read_arpost(db=db, arpost_id=comment_edit_form.arpost_id)
    if not check_arpost_id:
        raise HTTPException(status_code=400, detail="Not exists arpost_id.")

    # check comment_id
    check_comment_id = db_api.get_comment_arpost(db=db, arpost_id=comment_edit_form.arpost_id, comment_id=comment_edit_form.comment_id, username=username)
    if not check_comment_id:
        raise HTTPException(status_code=400, detail="This comment_id does not exist or is not authorized.")

    # length check
    if len(comment_edit_form.comment) > 512:
        raise HTTPException(status_code=400, detail="comment length < 512.")

    # edit comment
    edit_comment_success = db_api.edit_comment_arpost(db=db, arpost_id=comment_edit_form.arpost_id, comment_id=comment_edit_form.comment_id, comment=comment_edit_form.comment, username=username)

    # return
    if edit_comment_success:
        return {"detail":"edit arpost_comment success","arpost_id":edit_comment_success.arpost_id}
    else:
        raise HTTPException(status_code=400, detail="add arpost_comment  error.")

    return username

@app.post("/arpost/comment/delete")
def ar_post_comment_delete(comment_delete_form: schemas.ARpostCommentDelete, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = authentication.check_credentials(token)
    
    # check arpost_id
    check_arpost_id = db_api.read_arpost(db=db, arpost_id=comment_delete_form.arpost_id)
    if not check_arpost_id:
        raise HTTPException(status_code=400, detail="Not exists arpost_id.")

    # check comment_id and permission
    check_comment_id = db_api.get_comment_arpost(db=db, arpost_id=comment_delete_form.arpost_id, comment_id=comment_delete_form.comment_id, username=username)
    if not check_comment_id:
        raise HTTPException(status_code=400, detail="This comment_id does not exist or is not authorized.")
    
    # delete comment
    db_api.delete_comment_arpost(db=db, arpost_id=comment_delete_form.arpost_id, comment_id=comment_delete_form.comment_id, username=username)

    return {"detail":"delete arpost_comment success.","arpost_id":comment_delete_form.arpost_id, "comment_id":comment_delete_form.comment_id}
    

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=9999, reload=True)