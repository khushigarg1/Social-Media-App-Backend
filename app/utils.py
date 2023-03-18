
from passlib.context import CryptContext
# bcrypt is a algorithm for password hashing that we want to do like we dont want to store actual psw in our database so we will store psw with hashing and that will verify psw
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)
