import datetime
import sys
sys.path.append("..")

from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
import models
from utils.question_utils import Question, QuestionResponse, get_last_asked_question,\
    get_game, get_question_by_score, ResponseModel,\
    QuestionsResponseModel, QuestionItem, QuestionAdminResponseModel


async def read_all_questions(db: Session) -> QuestionsResponseModel:
    questions = db.query(models.Question.id_question, models.Question.question, models.Question.level).all()
    question_list = [QuestionItem(id_question=question.id_question,
                                  question=question.question,
                                  level=question.level)
                     for question in questions]
    return QuestionsResponseModel(questions=question_list)


async def get_question_by_id(id_question: int, db: Session) -> QuestionAdminResponseModel:
    question_model = db.query(models.Question).filter(models.Question.id_question == id_question).first()
    if question_model is None:
        raise HTTPException(status_code=404, detail="Question not found")
    user = db.query(models.User.username).filter(models.User.id_user == question_model.id_user).first()

    question_response = QuestionAdminResponseModel(
        id_question=question_model.id_question,
        question=question_model.question,
        choices=question_model.choices,
        level=question_model.level,
        correct_answer=question_model.correct_answer,
        auther=user.username,
        created_at=question_model.created_at
    )
    return question_response


async def get_question(user: dict, db: Session):
    game = get_game(user.get('id_user'), db)
    asked_question = get_last_asked_question(game.id_game, db)
    if asked_question is not None and asked_question.answer is None:
        question_model = db.query(models.Question).filter(models.Question.id_question == asked_question.id_question).first()

        if question_model is None:
            raise HTTPException(status_code=404, detail="Question not found")

        question_response = QuestionResponse(
            question=question_model.question,
            choices=question_model.choices,
            level=question_model.level
        )
        return question_response

    if game.ended_at is not None:
        raise HTTPException(status_code=400, detail="You need to start a game first")
    question_model = get_question_by_score(user.get("id_user"), game.score, game.id_game, db)

    asked_question_model = models.Asked_question(
        id_game=game.id_game,
        id_question=question_model.id_question,
        created_at=datetime.utcnow()
    )

    db.add(asked_question_model)
    db.commit()

    question_response = QuestionResponse(
        question=question_model.question,
        choices=question_model.choices,
        level=question_model.level
    )

    return question_response


async def add_question(question: Question, admin: dict, db: Session):
    model_question = models.Question(
        question=question.question,
        choices=question.choices,
        correct_answer=question.correct_answer,
        level=question.level,
        id_user=admin.get('id_user'),
        created_at=datetime.utcnow()
    )
    db.add(model_question)
    db.commit()

    return ResponseModel(status=status.HTTP_201_CREATED, message="Question added successfully")


async def update_question(id_question: int, question: Question, db: Session):
    model_question = db.query(models.Question).filter(models.Question.id_question == id_question).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    model_question.question = question.question
    model_question.choices = question.choices
    model_question.correct_answer = question.correct_answer
    model_question.level = question.level

    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question updated successfully")


async def delete_question(id_question: int, db: Session):
    model_question = db.query(models.Question).filter(models.Question.id_question == id_question).first()
    if model_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(model_question)
    db.commit()
    return ResponseModel(status=status.HTTP_200_OK, message="Question deleted successfully")
