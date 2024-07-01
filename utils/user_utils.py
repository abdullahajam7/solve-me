import sys
from pydantic import BaseModel
from datetime import datetime
from typing import List

sys.path.append("..")


class UserItem(BaseModel):
    id_user: int
    username: str


class UsersResponseModel(BaseModel):
    users: List[UserItem]


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


class UserGameStatsResponseModel(BaseModel):
    username: str
    max_score: int
    score: int


class ResponseModel(BaseModel):
    status: int
    message: str


class UserResponseModel(BaseModel):
    id_user: int
    username: str
    role: str
    created_at: datetime

