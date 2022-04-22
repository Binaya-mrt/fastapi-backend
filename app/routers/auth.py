from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from requests import Session
from sqlalchemy.orm import Session

from app import utils
from .. import database, models, schemas
router = APIRouter(tags=["authentication"])


@router.post('/login')
def login(user_credentails: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentails.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid credentails")

    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(status_code=404, detail=f"Invalid credentails")

    return {"token": "fake-token"}
