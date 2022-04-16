from cgitb import text
from datetime import datetime
import imp
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

from psycopg2 import Timestamp
from .database import Base
from sqlalchemy import  Column,Integer,String,Boolean
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),server_default=func.now())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable=False)
    password = Column(String, nullable=False)
    email=Column(String,nullable=False,unique=True)
    created_at= Column(TIMESTAMP(timezone=True),server_default=func.now())
        