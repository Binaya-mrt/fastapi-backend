from fastapi import FastAPI

from sqlalchemy.orm import Session
from .database import engine, get_db
from typing import List
from .routers import posts, users, auth

app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hey folks"}
