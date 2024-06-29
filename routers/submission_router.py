import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, verify_admin
from utils.submission_utils import SubmitResponseModel
from controllers.submission_controller import read_all_submissions, read_game_submissions_by_user, submit_answer, get_submission_by_id


# Initialize Router
router = APIRouter(
    prefix="/submissions",
    tags=["submissions"],
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
@router.get("/all")
async def read_all(user=Depends(verify_admin), db: Session = Depends(get_db)):
    return await read_all_submissions(db)


@router.get("/")
async def get_game_submissions_by_user(user_id: int, game_number: int, user=Depends(verify_admin), db: Session = Depends(get_db)):
    return await read_game_submissions_by_user(user_id, game_number, db)


@router.get("/{submission_id}")
async def get_by_id(submission_id: int, user=Depends(verify_admin), db: Session = Depends(get_db)):
    return await get_submission_by_id(submission_id, db)


@router.post("/submit", response_model=SubmitResponseModel)
async def submit(answer: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await submit_answer(answer, user, db)