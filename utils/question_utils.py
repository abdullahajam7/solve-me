# utils/question_utils.py

from pydantic import BaseModel
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
import random
from fastapi import HTTPException


class Question(BaseModel):
    question: str
    choices: dict
    correct_answer: str
    level: str


class QuestionResponse(BaseModel):
    question: str
    choices: Dict[str, str]
    level: str


class ResponseModel(BaseModel):
    status: int
    message: str


class SubmitResponseModel(BaseModel):
    status: int
    message: str
    correct: bool


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
