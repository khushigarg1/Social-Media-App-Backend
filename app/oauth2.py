# we have all the security flow, let's make the application actually secure, using JWT tokens and secure password hashing.

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# ------------secret key
# ------------algorithm
# ------------expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    # -------------we have to provide 30 minutes from now
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# -----------to verify access token string token and credentials exception should be passed


def verify_access_token(token: str, credentials_exception):

    try:
        # ------we have to decode where token secret key and algo which is used extract all payload data userid into id
        # print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        # ----------if not thenr aise exception
        if id is None:
            raise credentials_exception
        # -------validating data
        token_data = schemas.TokenData(id=id)

    except JWTError:
        # print(e)
        raise credentials_exception
    # except AssertionError as e:
    #     print(e)

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # return verify_access_token(token, credentials_exception)

    # ----------we want to calld irectly verify function and want that if it verifies access token then current user function should fetch the user from database, that means we can attach user to any path operations , we can fetch differently for diff functions
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
