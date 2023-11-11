from typing import List

from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import users
from sqlalchemy.orm import Session

from utils.utils import hash_password



router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=users.UserGet)
def create_user(user: users.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=users.UserGet)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists.")
    return user