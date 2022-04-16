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
from .routers import posts,users

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


app.include_router(posts.router)   
app.include_router(users.router)    
@app.get("/")
def root():
    return {"message": "Hey folks"}  

