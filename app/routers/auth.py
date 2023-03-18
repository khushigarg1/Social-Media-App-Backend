from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
# from ..database import get_db
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

# ---we have to fetch user data from user database so we have to import db session in it

# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
# ----------dependency with database to retreive data and automatically storing data into user-credentials


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # #------username  and password onauth2[asswordreqform send data into 2 var username and apssword it can be email user id and whatever]
    # {
    #     "username": "adsada",
    #     "password": "adsad"
    # }
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    # create and return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":  access_token, "token_type": "bearer"}
