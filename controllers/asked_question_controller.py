import datetime
import sys
sys.path.append("..")

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
from utils.asked_question_utils import SubmitResponseModel, get_current_question
from utils.question_utils import get_game
from datetime import datetime


async def read_all_submissions(db: Session):
    return db.query(models.Asked_question).all()


async def read_game(id_game: int, db: Session):
    return db.query(models.Asked_question).filter(models.Asked_question.id_game == id_game).all()


async def get_submission_by_id(id_asked_question: int, db: Session):
    submission_model = db.query(models.Asked_question).filter(models.Asked_question.id_asked_question == id_asked_question).first()
    if submission_model is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission_model


async def submit_answer(answer: int, user: dict, db: Session):
    game = get_game(user.get('id_user'), db)
    current_asked_question = get_current_question(game.id_game, db)
    if current_asked_question.answered_at is not None:
        raise HTTPException(status_code=404, detail="No question asked")
    id_question = current_asked_question.id_question
    question_model = db.query(models.Question).filter(models.Question.id_question == id_question).first()

    if question_model is None:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = False
    if answer == question_model.correct_answer:
        game.score = game.score + 1
        correct = True
    else:
        game.ended_at = datetime.utcnow()

    current_asked_question.answer = answer
    current_asked_question.answered_at = datetime.utcnow()
    db.commit()
    return SubmitResponseModel(status=status.HTTP_200_OK, message="Answer submitted successfully", correct=correct)
