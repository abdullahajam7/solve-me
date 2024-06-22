import sys
sys.path.append("..")

from typing import Optional, List
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from .auth import get_current_user, get_current_admin
from sqlalchemy import text
import random
import json


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


# Pydantic Models
class Question(BaseModel):
    question: str
    choices: dict
    correct_answer: str
    level: str


class QuestionResponse(BaseModel):
    question: str
    choices: dict
    level: str


class ResponseModel(BaseModel):
    status: int
    message: str


class SubmitResponseModel(BaseModel):
    status: int
    message: str
    correct: bool


# Helper Function to Get Question by Score
def get_question_by_score(score: int, user_id: int, game_number: int, db: Session):
    if score < 30:
        level = "easy"
    elif score < 70:
        level = "medium"
    else:
        level = "hard"

    # Query to get the number of available records
    count_query = text(f"""
        SELECT (
            (SELECT COUNT(*) FROM questions WHERE level = :level) - 
            (
                SELECT COUNT(*) 
                FROM submissions AS s
                JOIN questions q ON q.id = s.question_id
                WHERE q.level = :level AND s.user_id = :user_id AND s.game_number = :game_number
            )
        ) AS res
    """)
    count_result = db.execute(count_query, {'level': level, 'user_id': user_id, 'game_number': game_number}).fetchone()
    available_count = count_result[0] if count_result else 0
    if available_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    random_index = random.randint(0, available_count - 1)

    # Query to get the random question
    question_query = text(f"""
        SELECT id
        FROM questions 
        WHERE level = :level
        AND id NOT IN (
            SELECT question_id 
            FROM submissions 
            WHERE game_number = :game_number AND user_id = :user_id
        )
        LIMIT 1 OFFSET :random_index
    """)
    question_id_model = db.execute(question_query, {'level': level, 'user_id': user_id, 'game_number': game_number, 'random_index': random_index}).fetchone()

    if question_id_model is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question_id_model.id


# Routes
@router.get("/all")
async def read_all_questions(user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(models.Questions).all()


@router.get("/{question_id}", response_model=Question)
async def get_question_by_id(question_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    question_model = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if question_model is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question_model


#response_model=QuestionResponse
@router.get("/")
async def get_question(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    question_id = user.get("last_asked_question")
    if question_id == 0:
        question_id = get_question_by_score(user.get("score"), user.get("id"), user.get("games_played"), db)
        user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

        user_model.last_asked_question = question_id
        db.commit()

    question_model = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    question_response = QuestionResponse(
        question=question_model.question,
        choices=question_model.choices,
        level=question_model.level
    )

    return question_response


@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def add_question(question: Question, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    model_question = models.Questions(
        question=question.question,
        choices=question.choices,
        correct_answer=question.correct_answer,
        level=question.level
    )
    db.add(model_question)
    db.commit()

    return ResponseModel(status=status.HTTP_201_CREATED, message="Question added successfully")


@router.put("/{question_id}", response_model=ResponseModel)
async def update_question(question_id: int, question: Question, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    model_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    model_question.question = question.question
    model_question.choices = question.choices
    model_question.correct_answer = question.correct_answer
    model_question.level = question.level

    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question updated successfully")


@router.delete("/{question_id}", response_model=ResponseModel)
async def delete_question(question_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    model_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(model_question)
    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question deleted successfully")


@router.post("/submit", response_model=SubmitResponseModel)
async def submit_answer(answer: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    if user_model.last_asked_question == 0:
        raise HTTPException(status_code=404, detail="No question asked")
    question_id = user_model.last_asked_question
    question_model = db.query(models.Questions).filter(models.Questions.id == question_id).first()

    if question_model is None:
        raise HTTPException(status_code=404, detail="Question not found")

    submission_model = models.Submissions(user_id=user.get("id"), question_id=question_id, answer=answer, game_number=user_model.games_played)
    db.add(submission_model)

    correct = False
    if answer == question_model.correct_answer:
        if user_model.current_score == user_model.max_score:
            user_model.current_score += 1
            user_model.max_score += 1
        else:
            user_model.current_score += 1
        correct = True
    else:
        user_model.current_score = 0
        user_model.games_played += 1

    user_model.last_asked_question = 0
    db.commit()
    return SubmitResponseModel(status=status.HTTP_200_OK, message="Answer submitted successfully", correct=correct)

