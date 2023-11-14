from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from core import database, models
from schemas import auth
from utils import utils

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: auth.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return {"token": "example_token"}
