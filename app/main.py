from fastapi import FastAPI

from .database import engine, get_db
from . import models
from typing import List
from .routers import posts, users, auth, votes

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hey folks"}
