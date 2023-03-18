# firstly import fastapi
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi import Body
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

# create an instance of fastapi
app = FastAPI()

# # Dependency:- connection to a databse or session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# a post which is extracting basemodel
# -----------------------------schema---------------


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
# rating: Optional[int] = None


# we have to make a connection requires host that is ip address specific database to connect, username and password      The RealDictCursor class is being used as the cursor factory to create a cursor object that returns rows as dictionaries,
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


my_posts = [{"title": "post1", "content": "post1content", "id": 1},
            {"title": "favfood", "content": "pizza", "id": 2}]

# --------------finding post by id name


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# finding index for deleting a post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# This code defines an asynchronous Python function called root() using the async def
#  key-value pair with the key "message" and the value "Hello World".

# get is a method and "/" is a path and root is a function
# @is a decorator signature it is referenced with our fastapi instance which is app and our http get method and then specific path with root url

# request Get method url: "/"


@app.get("/")
async def root():
    return {"message": "Hello world"}


# sqlalchemy database connection which is making table by creating connection  with database
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # access to models and every entry which is in our Post table
    posts = db.query(models.Post).all()
    return {"data": posts}


# -------------anytime we amke chnages e have to restart our server
# --reload will automatically restart our server after changing anything

# for retrieving data we moslty use get
@app.get("/post")
# def get_posts():
# -------------- execture query with connection object cursor fetched all posts from databases socialmediapost
# cursor.execute(""" SELECT * from socialmediapost """)
# posts = cursor.fetchall()
# print(posts)
# return {"data": posts}
# return {"data": my_posts}
# -------------with sqlalchemy
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# ---------if both path are same then first  fucntion will run order amtters here

# ----------- it is going to extract all of the field from the body and converting to a pyhton dictionary and store in variable payload


# async def create_posts(payload: dict = Body(...)):
    # -------- here we extracted the data from the bod of the payload
    # print(payload)
    # return {"message": "successfully created post"}
    # return {"new_post": f"title: {payload['title']} content:{payload['content']}"}


# title str, content str, cactegory , bool published post
@app.post("/post", status_code=status.HTTP_201_CREATED)
# def create_posts(new_post: Post):
# print(new_post)
# ---------pydantic mpdel that is converting to dictionary which prints all properties
# print(new_post.dict())
# return {"data": new_post}
# -----------------------------retrieving all posts by my_posts we are appending all new posts which are creating by post fucntion and we are making new idd for every post with post+dict fucntion--------------------
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    # ---------from databases
    # cursor.execute(f"INSERT INTO socialmediapost (title, content, published) VALUES({post.title}, {post.content}, {post.published})")
    # cursor.execute("""INSERT INTO socialmediapost (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # --------- we have to do commit with connection to save our data in database
    # conn.commit()

    # ----------with sqlalchemy
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    # print(new_post)
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    db.add(new_post)  # ----added to database
    db.commit()  # ----commit to a database retrieve the new post
    db.refresh(new_post)  # -----store back to the var new_post
    return {"data": new_post}
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # return {"data": my_posts}
    # return {"data": post_dict}


# @app.get("/post/latest")
# def getlatest_post():
#     latpost = my_posts[len(my_posts) - 1]
#     return {"details": latpost}


# ------------------------retrieving one individual post with id name-----------------
# we are going to extract post with id number
@app.get("/post/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # ------------with sql
    # cursor.execute(
    #     """SELECT * FROM socialmediapost where id = %s """, (str(id),))
    # post = cursor.fetchone()

    # print(test_post)
    # print(id)
    # we have to convert id into int bcoz it is in string type
    # post = find_post(id)

    # ----------sqlalchemy here filtering post by id and then we know one id can only be of one post so .first() to send the query if we know id is primary
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # # response.status_code = 404
    # return {"message": f"post with id: {id} was not found"}
    # ----------------better way to do -------------
    return {"post_details": post}


# ----------------------Deleting post--------------
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # ----------------sql
    # cursor.execute(
    #     """DELETE FROM socialmediapost where id = %s returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()

    # deleting post
    # find the index in the array that has required id
    # my_posts.pop(index)
    # index = find_index_post(id)
    # if index == None:

    # --------------sqlalachemy
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    # return {"message": 'successfully deleted'}
    # if we use status code 204 then fastapi wont send any message back so we have to use diff type of respone
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------updating post----------------
# user is sending put request to a specific id find index of specific post if not exist then error or if exist then take data from frontend which alreayd exists from Post convert to post_dictional of python then put id into post_dict[id] then replace my_post with updated post
@app.put("/post/{id}")
# def update_post(id: int, post: Post, db: Session = Depends(get_db)):
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    # ----------------------sql
    # cursor.execute("""UPDATE socialmediapost SET title = %s, content =%s, published = %s  WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # print(post)
    # index = find_index_post(id)

    # --------------------sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    # print(updated_post.dict())
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # post_query.update({'title': 'hey this is my updated title',
    #                    'content': 'this is my updated content'}, synchronize_session=False)
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return {'data': post_dict}
    return {"data": post_query.first()}
