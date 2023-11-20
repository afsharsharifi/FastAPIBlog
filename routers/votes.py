from core import database, models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import vote
from sqlalchemy.orm import Session
from utils import oauth2

router = APIRouter(tags=["Posts"], prefix="/vote")


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: vote.Vote,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    has_vote = vote_query.first()
    if not has_vote:
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"Successfully Liked Post with ID of {vote.post_id}"}
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Successfully Removed Like from Post with ID of {vote.post_id}"}
