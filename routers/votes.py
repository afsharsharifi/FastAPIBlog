from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import vote
from sqlalchemy.orm import Session
from utils import oauth2

router = APIRouter(tags=["Posts"], prefix="/vote")


@router.post("/like", status_code=status.HTTP_201_CREATED)
def like_post(
    vote: vote.Vote,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exists.")
    if post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cant Like Own Post")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    has_vote = vote_query.first()
    if has_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} has already liked post with id {vote.post_id}")
    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": f"Successfully Liked Post with ID of {vote.post_id}"}


@router.post("/dislike", status_code=status.HTTP_204_NO_CONTENT)
def dislike_post(
    vote: vote.Vote,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exists.")
    if post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cant Dislike Own Post")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    has_vote = vote_query.first()
    if not has_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User hasn't liked this post yet")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Successfully Removed Like from Post with ID of {vote.post_id}"}
