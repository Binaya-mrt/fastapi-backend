from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import setting

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ipaddress>/<database_name>"

SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True  :
#     try:
#         conn = psycopg2.connect(dbname='fastapi', user='postgres', password='swarga', host='localhost',cursor_factory= RealDictCursor)
#         cursor=conn.cursor()
#         print("Connected to database")
#         break
#     except Exception as error:
#         print ("Error while connecting to PostgreSQL", error)
#         time.sleep(3)
