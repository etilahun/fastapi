
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True 

class UserCreate(BaseModel):
  email: EmailStr 
  password: str

class UserResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

class PostCreate(PostBase):
  pass

class PostResponse(PostBase):
  id: int
  created_at: datetime
  user_id: int

class PostCountResponse(PostResponse):
  votes: int

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None

class Vote(BaseModel):
  post_id: int
  dir: conint(le=1) 