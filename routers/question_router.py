import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, get_current_admin
from utils.question_utils import Question, QuestionResponse, ResponseModel
from controllers.question_controller import read_all_questions, get_question, get_question_by_id
from controllers.question_controller import update_question, delete_question, add_question

# Initialize Router
router = APIRouter(
    prefix="/questions",
    tags=["questions"],
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


@router.get("/all")
async def read_all(user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await read_all_questions(user, db)


@router.get("/{question_id}", response_model=Question)
async def get_by_id(question_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await get_question_by_id(question_id, user, db)


@router.get("/", response_model=QuestionResponse)
async def ask(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await get_question(user, db)


@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def add(question: Question, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await add_question(question, user, db)


@router.put("/{question_id}", response_model=ResponseModel)
async def update(question_id: int, question: Question, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await update_question(question_id, question, user, db)


@router.delete("/{question_id}", response_model=ResponseModel)
async def delete(question_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await delete_question(question_id, user, db)