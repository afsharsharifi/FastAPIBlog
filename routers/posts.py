from typing import List, Optional

from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import post
from sqlalchemy.orm import Session
from utils import oauth2
from sqlalchemy import func

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("/", response_model=List[post.PostOut])
def get_posts(
    db: Session = Depends(database.get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("likes"))
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True,
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post.Post)
def create_post(
    post: post.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=post.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db)):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("likes"))
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True,
        )
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform Requested Action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post.Post)
def update_post(
    id: int,
    post: post.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_object = post_query.first()
    if post_object == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists.")

    if post_object.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform Requested Action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
