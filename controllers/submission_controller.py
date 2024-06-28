import sys
sys.path.append("..")

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
from utils.submission_utils import SubmitResponseModel


async def read_all_submissions(db: Session):
    return db.query(models.Submissions).all()


async def read_game_submissions_by_user(user_id: int, game_number: int, db: Session):
    return db.query(models.Submissions).filter(models.Submissions.game_number == game_number and models.Submissions.user_id == user_id).all()


async def get_submission_by_id(submission_id: int, db: Session):
    submission_model = db.query(models.Submissions).filter(models.Submissions.id == submission_id).first()
    if submission_model is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission_model


async def submit_answer(answer: str, user: dict, db: Session):
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

    submission_model.correct = correct
    user_model.last_asked_question = 0
    db.commit()
    return SubmitResponseModel(status=status.HTTP_200_OK, message="Answer submitted successfully", correct=correct)

