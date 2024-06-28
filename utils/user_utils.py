import sys
from pydantic import BaseModel

sys.path.append("..")


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


class ResponseModel(BaseModel):
    status: int
    message: str
