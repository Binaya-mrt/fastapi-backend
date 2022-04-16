from fastapi import FastAPI, Response, status,HTTPException,Depends
from pydantic import BaseModel
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models,schemas,utils
from typing import List  


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

while True  :
    try:
        conn = psycopg2.connect(dbname='fastapi', user='postgres', password='swarga', host='localhost',cursor_factory= RealDictCursor)
        cursor=conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print ("Error while connecting to PostgreSQL", error)
        time.sleep(3)   
@app.get("/")
def root():
    return {"message": "Hey folks"}  

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    posts= db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #  (post.title, post.content, post.published))
    # new_post= cursor.fetchone()
    # conn.commit()
    # print(new_post)
    new_post= models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post     

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s""",(str(id),))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
       raise  HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first== None:
        raise HTTPException(status_code=404, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted"}   
    

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published,str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()
   
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if  post ==None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit() 
    return post_query.first()

# @app.post("/users",status_code=status.HTTP_201_CREATED)    
# def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):
#     # user=models.User(name="Test",email="
#     new_user= models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user  
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
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
