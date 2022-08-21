from typing import List, Union, Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class LoginForm(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    name: str
    email: str

class RegisterForm(UserBase):
    password: str

class ARpostCoordi(BaseModel):
    x_value: str
    y_value: str

class ARpostId(BaseModel):
    arpost_id: int

class ARpostEmotion(BaseModel):
    arpost_id: int
    emotion: str

class ARpostComment(BaseModel):
    arpost_id: int
    comment: str

class ARpostCommentEdit(BaseModel):
    arpost_id: int
    comment_id: int
    comment: str

class ARpostCommentDelete(BaseModel):
    arpost_id: int
    comment_id: int