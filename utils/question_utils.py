from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
import random
from fastapi import HTTPException

import models


class Question(BaseModel):
    question: str
    choices: dict
    correct_answer: int
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


def get_game(id_user: int, db: Session):
    subquery = db.query(func.max(models.Game.id_game)).filter(models.Game.id_user == id_user).scalar_subquery()
    game = db.query(models.Game).filter(models.Game.id_user == id_user, models.Game.id_game == subquery).one_or_none()

    if game is None:
        raise HTTPException(status_code=404, detail="No game started")
    return game


def get_last_asked_question(id_game: int, db: Session):
    subquery = db.query(func.max(models.Asked_question.id_asked_question)).filter(
        models.Asked_question.id_game == id_game).scalar_subquery()

    asked_question = db.query(models.Asked_question).filter(
        models.Asked_question.id_game == id_game, models.Asked_question.id_asked_question == subquery).one_or_none()

    return asked_question


def get_question_by_score(id_user: int, score: int, id_game: int, db: Session):
    if score < 30:
        level = "easy"
    elif score < 70:
        level = "medium"
    else:
        level = "hard"

    total_questions_subquery = db.query(func.count(models.Question.id_question)).filter(
        models.Question.level == level).scalar_subquery()

    asked_questions_subquery = db.query(func.count(models.Asked_question.id_asked_question)).join(models.Question)\
        .filter(models.Question.level == level, models.Asked_question.id_game == id_game)\
        .scalar_subquery()

    # Final query to get the difference
    count_result = db.query(total_questions_subquery - asked_questions_subquery).scalar()

    if count_result == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    random_index = random.randint(0, count_result - 1)

    subquery = db.query(models.Question.id_question).filter(
        models.Question.level == level,
        ~models.Question.id_question.in_(
            db.query(models.Asked_question.id_question).join(models.Game).filter(
                models.Asked_question.id_game == id_game,
                models.Game.id_user == id_user
            )
        )
    ).limit(1).offset(random_index).subquery()

    question = db.query(models.Question).filter(models.Question.id_question == subquery.c.id_question).one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
