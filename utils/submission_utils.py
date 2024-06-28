import sys
sys.path.append("..")

from pydantic import BaseModel


class SubmitResponseModel(BaseModel):
    status: int
    message: str
    correct: bool

