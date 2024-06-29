from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from models import User
from utils.auth_utils import CreateUser, get_password_hash, authenticate_user, create_access_token, token_exception


async def create_new_user(create_user: CreateUser, db: Session):
    create_user_model = User()
    create_user_model.username = create_user.username
    create_user_model.created_at = datetime.utcnow()
    create_user_model.role = "user"

    hashed_password = get_password_hash(create_user.password)
    create_user_model.hashed_password = hashed_password

    db.add(create_user_model)
    db.commit()


async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user: User = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(hours=10)
    token = create_access_token(user.role, user.id_user, expires_delta=token_expires)
    return {"token": token}
