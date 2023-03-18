
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# -------REsponse


class Post(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut

    # title: str
    # content: str
    # published: bool
# to convert sqlalchemy model into pydantic model bcoz it is not a dictionary it is a sqlalchemy model so to convert into pydantic model ormmode true

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# --------------user schema-----


class UserCreate(BaseModel):
    email: EmailStr
    password: str


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
    # --------lessthan andequal to 1 vote can be 0 or 1 for any post of user
    dir: conint(le=1)
