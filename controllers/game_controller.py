import datetime
import sys
sys.path.append("..")

from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from utils.game_utils import ResponseModel, get_game
from datetime import datetime


async def read_all_games(db: Session):
    return db.query(models.Game).all()


async def read_all_games_by_user(id_user: int, db: Session):
    return db.query(models.Game).filter(models.Game.id_user == id_user).all()


async def read_game_by_id(id_game: int, db: Session):
    game_model = db.query(models.Game).filter(models.Game.id_game == id_game).first()
    if game_model is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game_model


async def start_game(id_user: int, db: Session):
    game = get_game(id_user, db)
    if game is not None and game.ended_at is None:
        raise HTTPException(status_code=400, detail="Your game is still running!")
    game = models.Game(
        id_user=id_user,
        score=0,
        created_at=datetime.utcnow()
    )
    db.add(game)
    db.commit()
    response_model = ResponseModel(status=200, message="game started successfully")
    return response_model
