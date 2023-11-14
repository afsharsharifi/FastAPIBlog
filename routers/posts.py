from typing import List

from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import post
from sqlalchemy.orm import Session
from utils import oauth2

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("/", response_model=List[post.Post])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post.Post)
def create_post(
    post: post.PostCreate,
    db: Session = Depends(database.get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=post.Post)
def get_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post.Post)
def update_post(id: int, post: post.PostCreate, db: Session = Depends(database.get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_object = post_query.first()
    if post_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
