import sys
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
from utils.auth_utils import verify_password, get_password_hash
from utils.user_utils import ResponseModel, UserVerification

sys.path.append("..")


async def read_all_users(db: Session):
    users = db.query(models.User).all()
    return users


async def read_user(id_user: int, db: Session):
    user_model = db.query(models.User).filter(models.User.id_user == id_user).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


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


async def make_admin(user_id: int, db: Session):
    user_model = db.query(models.User).filter(models.User.id_user == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.role = "admin"
    db.commit()

    return ResponseModel(status=status.HTTP_200_OK, message="User promoted to admin successfully")
