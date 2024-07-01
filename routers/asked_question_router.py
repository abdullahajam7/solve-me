import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, verify_admin
from controllers.asked_question_controller import read_all_submissions, read_game, submit_answer, get_submission_by_id, SubmitResponseModel


# Initialize Router
router = APIRouter(
    prefix="/asked_question",
    tags=["asked_question"],
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
    return await read_all_submissions(db)


@router.get("/", dependencies=[Depends(verify_admin)])
async def get_game_info(id_game: int, db: Session = Depends(get_db)):
    return await read_game(id_game, db)


@router.get("/{id_asked_question}", dependencies=[Depends(verify_admin)])
async def get_by_id(id_asked_question: int, db: Session = Depends(get_db)):
    return await get_submission_by_id(id_asked_question, db)


@router.post("/submit", response_model=SubmitResponseModel)
async def submit(answer: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await submit_answer(answer, user, db)
