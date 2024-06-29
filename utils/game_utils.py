import sys
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

import models


sys.path.append("..")


class ResponseModel(BaseModel):
    status: int
    message: str


def get_game(id_user: int, db: Session):
    subquery = db.query(func.max(models.Game.id_game)).filter(models.Game.id_user == id_user).scalar_subquery()
    game = db.query(models.Game).filter(models.Game.id_user == id_user, models.Game.id_game == subquery).one_or_none()

    return game
