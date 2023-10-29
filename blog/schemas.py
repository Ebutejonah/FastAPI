from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username : str
    first_name : str
    last_name : str
    email : str
    password : str
    confirm_password : str


class Authenticate(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class Blog(BaseModel):
    title: str
    body : str

class UpdateBlog(BaseModel):
    title : Optional [str] = None
    body : Optional [str] = None
