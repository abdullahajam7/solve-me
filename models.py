from sqlalchemy import Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    current_score = Column(Integer)
    max_score = Column(Integer)
    games_played = Column(Integer)
    last_asked_question = Column(Integer)
    submissions = relationship("Submissions", back_populates="owner")


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True)
    choices = Column(JSON)
    correct_answer = Column(String)
    level = Column(String)
    submissions = relationship("Submissions", back_populates="question")

class Submissions(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    answer = Column(String)
    game_number = Column(Integer)
    correct = Column(Boolean)

    owner = relationship("Users", back_populates="submissions")
    question = relationship("Questions", back_populates="submissions")
