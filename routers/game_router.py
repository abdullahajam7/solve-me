import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, verify_admin
from controllers.game_controller import read_game_by_id, read_all_games, start_game, read_all_games_by_user


# Initialize Router
router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

# Create Database Tables
models.Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Routes
@router.get("/all", dependencies=[Depends(verify_admin)])
async def read_all(db: Session = Depends(get_db)):
    return await read_all_games(db)


@router.get("/", dependencies=[Depends(verify_admin)])
async def read_all_by_user(id_user, db: Session = Depends(get_db)):
    return await read_all_games_by_user(id_user, db)


@router.get("/{id_game}", dependencies=[Depends(verify_admin)])
async def get_game_info(id_game: int, db: Session = Depends(get_db)):
    return await read_game_by_id(id_game, db)


@router.post("/")
async def new_game(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await start_game(user.get("id_user"), db)
