import sys
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from utils.auth_utils import verify_password, get_password_hash
from utils.user_utils import ResponseModel, UserVerification, UserResponseModel,\
    UsersResponseModel, UserGameStatsResponseModel

sys.path.append("..")


async def read_all_users(db: Session) -> UsersResponseModel:
    users = db.query(models.User.id_user, models.User.username).all()
    user_list = [{"id_user": user.id_user, "username": user.username} for user in users]
    return UsersResponseModel(users=user_list)


async def read_user(id_user: int, db: Session) -> UserResponseModel:
    user_model = db.query(
        models.User.id_user,
        models.User.username,
        models.User.role,
        models.User.created_at
    ).filter(models.User.id_user == id_user).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = UserResponseModel(
        id_user=user_model.id_user,
        username=user_model.username,
        role=user_model.role,
        created_at=user_model.created_at
    )

    return user_response


async def get_user_game_stats(id_user: int, db: Session) -> UserGameStatsResponseModel:
    # Get the user and their games
    user = db.query(models.User).filter(models.User.id_user == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    max_score = db.query(func.max(models.Game.score)).filter(models.Game.id_user == id_user).scalar() or 0

    last_game = db.query(models.Game).filter(models.Game.id_user == id_user).order_by(
        models.Game.id_game.desc()).first()

    if last_game and last_game.ended_at is None:
        current_score = last_game.score
    else:
        current_score = 0

    user_game_stats = UserGameStatsResponseModel(
        username=user.username,
        max_score=max_score,
        score=current_score
    )

    return user_game_stats


async def update_my_password(user_verification: UserVerification, cur_user: dict, db: Session):
    user_model = db.query(models.User).filter(models.User.id_user == cur_user.get('id_user')).first()

    if user_model is None or not verify_password(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid user or request")

    if user_model.username == user_verification.username:
        user_model.hashed_password = get_password_hash(user_verification.new_password)
        db.commit()
        return ResponseModel(status=status.HTTP_200_OK, message="Password updated successfully")

    raise HTTPException(status_code=400, detail="Invalid user or request")


async def delete_my_account(user: dict, db: Session):
    user_model = db.query(models.User).filter(models.User.id_user == user.get('id_user')).first()

    if user_model is None:
        raise HTTPException(status_code=400, detail="Invalid user or request")

    db.query(models.User).filter(models.User.id_user == user.get("id_user")).delete()
    db.commit()

    return ResponseModel(status=status.HTTP_200_OK, message="Account deleted successfully")


async def make_admin(id_user: int, db: Session):
    user_model = db.query(models.User).filter(models.User.id_user == id_user).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.role = "admin"
    db.commit()

    return ResponseModel(status=status.HTTP_200_OK, message="User promoted to admin successfully")
