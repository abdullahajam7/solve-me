import sys

import models

sys.path.append("..")

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException


class SubmitResponseModel(BaseModel):
    status: int
    message: str
    correct: bool


def get_game(id_user: int, db: Session):
    subquery = db.query(func.max(models.Game.id_game)).filter(models.Game.id_user == id_user).scalar_subquery()

    # Query the Game table using the subquery
    game = db.query(models.Game).filter(models.Game.id_user == id_user, models.Game.id_game == subquery).one_or_none()

    if game is None:
        raise HTTPException(status_code=404, detail="No game started")
    return game


def get_current_question(id_game: int, db: Session):
    subquery = db.query(func.max(models.Asked_question.id_asked_question)).filter(
        models.Asked_question.id_game == id_game).scalar_subquery()

    # Query to get the asked_question with the max id_asked_question
    asked_question = db.query(models.Asked_question).filter(
        models.Asked_question.id_game == id_game,
        models.Asked_question.id_asked_question == subquery
    ).one_or_none()

    return asked_question
