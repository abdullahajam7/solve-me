import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user, get_current_admin
from utils.user_utils import ResponseModel, UserVerification
from controllers.user_controller import read_all_users, read_user, update_my_password, delete_my_account, make_admin
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


@router.get("/")
async def read_all(user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await read_all_users(db)


@router.get("/{user_id}")
async def get_by_id(user_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await read_user(user_id, db)


@router.put("/password", response_model=ResponseModel)
async def update_password(user_verification: UserVerification, cur_user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    return await update_my_password(user_verification, cur_user, db)


@router.delete("/", response_model=ResponseModel)
async def delete_account(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await delete_my_account(user, db)


@router.put("/admin", response_model=ResponseModel)
async def add_admin(user_id: int, user: dict = Depends(get_current_admin), db: Session = Depends(get_db)):
    return await make_admin(user_id, db)

