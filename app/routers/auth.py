from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from requests import Session
from sqlalchemy.orm import Session

from app import utils
from .. import database, models, schemas, oath2
router = APIRouter(tags=["authentication"])


@router.post('/login')
def login(user_credentails: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentails.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid credentails")

    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(status_code=404, detail=f"Invalid credentails")
    access_token = oath2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}
