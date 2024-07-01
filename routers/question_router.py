import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, verify_admin
from utils.question_utils import Question, QuestionResponse, ResponseModel, QuestionsResponseModel
from controllers.question_controller import read_all_questions, get_question, get_question_by_id,\
    update_question, delete_question, add_question, QuestionAdminResponseModel

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


@router.get("/all", response_model=QuestionsResponseModel, dependencies=[Depends(verify_admin)])
async def read_all(db: Session = Depends(get_db)):
    return await read_all_questions(db)


@router.get("/{id_question}", response_model=QuestionAdminResponseModel, dependencies=[Depends(verify_admin)])
async def get_by_id(id_question: int, db: Session = Depends(get_db)):
    return await get_question_by_id(id_question, db)


@router.get("/", response_model=QuestionResponse)
async def ask(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await get_question(user, db)


@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def add(question: Question, admin: dict = Depends(verify_admin), db: Session = Depends(get_db)):
    return await add_question(question, admin, db)


@router.put("/{id_question}", response_model=ResponseModel, dependencies=[Depends(verify_admin)])
async def update(id_question: int, question: Question, db: Session = Depends(get_db)):
    return await update_question(id_question, question, db)


@router.delete("/{id_question}", response_model=ResponseModel, dependencies=[Depends(verify_admin)])
async def delete(id_question: int, db: Session = Depends(get_db)):
    return await delete_question(id_question, db)

