from .. import models, schemas, oath2, database
from fastapi import Response, status, HTTPException, Depends, APIRouter


from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED,)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    vote_found = vote_query.first()
    if(vote.dir == 1):
        if vote_found:
            raise HTTPException(
                status_code=400, detail="You have already voted")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        print(new_vote)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not vote_found:
            raise HTTPException(
                status_code=400, detail="You have not voted yet")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}

    return {"message": "success"}
