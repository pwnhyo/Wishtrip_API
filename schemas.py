from typing import List, Union
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

class ARpostForm(BaseModel):
    name: str
    contents: str
    x_value: float
    y_value: float
    z_value: float
    #datetime
    #username

class ARpostCoordi(BaseModel):
    x_value: float
    y_value: float

class ARpostId(BaseModel):
    arpost_id: int

class ARpostComment(BaseModel):
    arpost_id: int
    comment: str

class ARpostCommentEdit(BaseModel):
    arpost_id: int
    comment_id: int
    comment: str