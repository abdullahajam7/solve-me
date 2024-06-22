import sys
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from .auth import get_current_user, verify_password, get_password_hash, get_current_admin

sys.path.append("..")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


class ResponseModel(BaseModel):
    status: int
    message: str


@router.get("/")
async def read_all_users(user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/{user_id}")
async def read_user(user_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.put("/password", response_model=ResponseModel)
async def update_password(user_verification: UserVerification, cur_user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == cur_user.get('id')).first()

    if user_model is None or not verify_password(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid user or request")

    if user_model.username == user_verification.username:
        user_model.hashed_password = get_password_hash(user_verification.new_password)
        db.commit()
        return ResponseModel(status=status.HTTP_200_OK, message="Password updated successfully")

    raise HTTPException(status_code=400, detail="Invalid user or request")


@router.delete("/", response_model=ResponseModel)
async def delete_my_account(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=400, detail="Invalid user or request")

    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()

    return ResponseModel(status=status.HTTP_200_OK, message="Account deleted successfully")


@router.put("/admin", response_model=ResponseModel)
async def make_admin(user_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.role = "admin"
    db.commit()

    return ResponseModel(status=status.HTTP_200_OK, message="User promoted to admin successfully")
