from fastapi import Depends, HTTPException, status
from blog import models, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from blog.database import get_db
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def get_user_by_username(username:str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username == username).first()

def get_current_user(token_code: str=Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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
