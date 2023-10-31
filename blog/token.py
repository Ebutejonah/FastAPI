from datetime import datetime, timedelta
from jose import JWTError, jwt
from blog import schemas
from sqlalchemy.orm import Session
from blog import models
from fastapi import Depends
from blog.database import get_db


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_by_username(username:str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username == username).first()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token_code:str, credentials_exception, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token_code, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username, db)
    if user is None:
        raise credentials_exception
    return user