import sys
sys.path.append("..")

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
from utils.question_utils import Question, QuestionResponse, ResponseModel, get_question_by_score


async def read_all_questions(user: dict, db: Session):
    return db.query(models.Questions).all()


async def get_question_by_id(question_id: int, user: dict, db: Session):
    question_model = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if question_model is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question_model


async def get_question(user: dict, db: Session):
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


async def add_question(question: Question, user: dict, db: Session):
    model_question = models.Questions(
        question=question.question,
        choices=question.choices,
        correct_answer=question.correct_answer,
        level=question.level
    )
    db.add(model_question)
    db.commit()

    return ResponseModel(status=status.HTTP_201_CREATED, message="Question added successfully")


async def update_question(question_id: int, question: Question, user: dict, db: Session):
    model_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    model_question.question = question.question
    model_question.choices = question.choices
    model_question.correct_answer = question.correct_answer
    model_question.level = question.level

    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question updated successfully")


async def delete_question(question_id: int, user: dict, db: Session):
    model_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(model_question)
    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question deleted successfully")
