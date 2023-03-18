from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# have to create a engine to connect sqlalchemy to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# when we have to talk actually to datatabse so need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency:- connection to a databse or creating session to database fro every request


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgreSql#13',  cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successfull")
        break
    except Exception as error:
        print("connection failed")
        print("Error", error)
        # the error message associated with the exception that was raised. It then waits for two seconds and tries to connect again in an infinite loop until a successful connection is made.
        time.sleep(2)
