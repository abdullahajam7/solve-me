from typing import Optional
from fastapi import FastAPI
import models
from database import engine
from routers import auth_router, user_router, question_router, asked_question_router, game_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(question_router.router)
app.include_router(asked_question_router.router)
app.include_router(game_router.router)

