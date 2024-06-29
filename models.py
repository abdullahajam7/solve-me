from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import JSON
from database import Base


class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime)


class Question(Base):
    __tablename__ = "question"

    id_question = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id_user"))
    question = Column(String, unique=True)
    choices = Column(JSON)
    correct_answer = Column(Integer)
    level = Column(String)
    created_at = Column(DateTime)


class Game(Base):
    __tablename__ = "game"

    id_game = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id_user"))
    score = Column(Integer)
    created_at = Column(DateTime)
    ended_at = Column(DateTime)


class Asked_question(Base):
    __tablename__ = "asked_question"

    id_asked_question = Column(Integer, primary_key=True)
    id_game = Column(Integer, ForeignKey("game.id_game"))
    id_question = Column(Integer, ForeignKey("question.id_question"))
    answer = Column(Integer)
    created_at = Column(DateTime)
    answered_at = Column(DateTime)
