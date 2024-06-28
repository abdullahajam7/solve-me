from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models import Users
from utils.auth_utils import CreateUser, get_password_hash, authenticate_user, create_access_token, token_exception


async def create_new_user(create_user: CreateUser, db: Session):
    create_user_model = Users()
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.email = create_user.email
    create_user_model.role = "user"
    create_user_model.max_score = 0
    create_user_model.current_score = 0
    create_user_model.games_played = 0
    create_user_model.last_asked_question = 0

    hashed_password = get_password_hash(create_user.password)
    create_user_model.hashed_password = hashed_password

    db.add(create_user_model)
    db.commit()


async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user: Users = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}
