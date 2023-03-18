# firstly import fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# for retrieving data we moslty use get


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # ---------pots?limit=2&skip=2&search=title

    # posts = db.query(models.Post).filter(
    # models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # -----------select eveything from post tables
    # #-----------left outer join group by post id of Post table
    # #----------------------SELECT socialmediapost.id AS socialmediapost_id, socialmediapost.title AS socialmediapost_title, socialmediapost.content AS socialmediapost_content, socialmediapost.published AS socialmediapost_published, socialmediapost.created_at AS socialmediapost_created_at, socialmediapost.owner_id AS socialmediapost_owner_id, count(votes.post_id) AS votes
    # FROM socialmediapost LEFT OUTER JOIN votes ON votes.post_id = socialmediapost.id GROUP BY socialmediapost.id

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(results)

    # posts = db.query(models.Post).all()
    # ----------for finding only that post which is created by that user whihc is erquesting to get posts
    # posts = db.query(models.Post).filter(
    # models.Post.owner_id == current_user.id).all()
    return results
    # return {"data": posts}


# title str, content str, cactegory , bool published post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(current_user.email)
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # new_post.owner_id = current_user.id
    db.add(new_post)  # ----added to database
    db.commit()  # ----commit to a database retrieve the new post
    db.refresh(new_post)  # -----store back to the var new_post
    return new_post


# ------------------------retrieving one individual post with id name-----------------
# we are going to extract post with id number
# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorised to perform requested action")

    return post


# ----------------------Deleting post--------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------updating post----------------
# user is sending put request to a specific id find index of specific post if not exist then error or if exist then take data from frontend which alreayd exists from Post convert to post_dictional of python then put id into post_dict[id] then replace my_post with updated post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    # print(updated_post.dict())
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
