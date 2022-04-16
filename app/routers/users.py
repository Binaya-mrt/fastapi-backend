
from .. import models,schemas,utils
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session
from ..database import get_db

from typing import List  
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/',response_model=List[schemas.UserOut])
def get_all_user(db:Session=Depends(get_db)):
    user=db.query(models.User).all()
    return user    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user= models.User(**user.dict())
    if new_user.email in (user.email for user in db.query(models.User).all()):
        raise HTTPException(status_code=400, detail="Email already registered")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} not found")
    return user
