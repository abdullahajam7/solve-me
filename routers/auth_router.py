from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth_controller import create_new_user, login_for_access_token
from utils.auth_utils import get_db
from utils.auth_utils import CreateUser

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"description": "Not Authorized"}}
)


@router.post("/signup")
async def signup(create_user: CreateUser, db: Session = Depends(get_db)):
    await create_new_user(create_user, db)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await login_for_access_token(form_data, db)
