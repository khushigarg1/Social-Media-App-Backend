# firstly import fastapi
# from typing import Optional, List
from fastapi import FastAPI
# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi import Body
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models
from .database import engine
# from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)
# from pydantic import BaseSettings


# class Settings(BaseSettings):
#     database_password: str
#     database_username: str = "postgres"
#     secret_key: str = "j13291ej930298492je02i93"


# settings = Settings()


# print(settings.path)

# -----router is just to split all our path operations in diff diff files
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------fastapi object it will give http request to post.py and can access all of the routers of post and usr file
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='postgreSql#13',  cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection successfull")
#         break
#     except Exception as error:
#         print("connection failed")
#         print("Error", error)
#         # the error message associated with the exception that was raised. It then waits for two seconds and tries to connect again in an infinite loop until a successful connection is made.
#         time.sleep(2)


# my_posts = [{"title": "post1", "content": "post1content", "id": 1},
#             {"title": "favfood", "content": "pizza", "id": 2}]

# --------------finding post by id name


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# finding index for deleting a post


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# -------------anytime we amke chnages e have to restart our server
# --reload will automatically restart our server after changing anything

# # for retrieving data we moslty use get
# @app.get("/post", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
#     # return {"data": posts}


# # title str, content str, cactegory , bool published post
# @app.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)  # ----added to database
#     db.commit()  # ----commit to a database retrieve the new post
#     db.refresh(new_post)  # -----store back to the var new_post
#     return new_post


# # ------------------------retrieving one individual post with id name-----------------
# # we are going to extract post with id number
# @app.get("/post/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     return post


# # ----------------------Deleting post--------------
# @app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     deleted_post = db.query(models.Post).filter(models.Post.id == id)

#     if deleted_post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {id} does not exist")

#     deleted_post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# # ---------------updating post----------------
# # user is sending put request to a specific id find index of specific post if not exist then error or if exist then take data from frontend which alreayd exists from Post convert to post_dictional of python then put id into post_dict[id] then replace my_post with updated post
# @app.put("/post/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     updated_post = post_query.first()
#     # print(updated_post.dict())
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {id} does not exist")

#     post_query.update(post.dict(), synchronize_session=False)
#     db.commit()

#     return post_query.first()


# # ----------------------USER AUTHENTICATION---------------

# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     # -------------HASH THE PASSWORD - user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get('/users/{id}', response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id: {id} does not exist")

#     return user
