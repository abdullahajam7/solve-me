import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from utils.auth_utils import get_current_user_auth, verify_admin
from utils.user_utils import ResponseModel,\
    UserVerification, UserResponseModel, UsersResponseModel, UserGameStatsResponseModel
from controllers.user_controller import read_all_users, read_user, update_my_password,\
    delete_my_account, make_admin, get_user_game_stats
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


@router.get("/", response_model=UsersResponseModel, dependencies=[Depends(verify_admin)])
async def read_all(db: Session = Depends(get_db)):
    return await read_all_users(db)


@router.get('/me', response_model=UserGameStatsResponseModel)
async def get_my_stats(user: dict = Depends(get_current_user_auth), db: Session = Depends(get_db)):
    return await get_user_game_stats(user.get('id_user'), db)


@router.get("/{id_user}", response_model=UserResponseModel, dependencies=[Depends(verify_admin)])
async def get_by_id(id_user: int, db: Session = Depends(get_db)):
    return await read_user(id_user, db)


@router.put("/password", response_model=ResponseModel)
async def update_password(user_verification: UserVerification, cur_user: dict = Depends(get_current_user_auth),
                          db: Session = Depends(get_db)):
    return await update_my_password(user_verification, cur_user, db)


@router.delete("/", response_model=ResponseModel)
async def delete_account(user: dict = Depends(get_current_user_auth), db: Session = Depends(get_db)):
    return await delete_my_account(user, db)


@router.put("/admin", response_model=ResponseModel, dependencies=[Depends(verify_admin)])
async def add_admin(id_user: int, db: Session = Depends(get_db)):
    return await make_admin(id_user, db)

