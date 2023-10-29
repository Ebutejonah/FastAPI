from fastapi import APIRouter, status, HTTPException, Depends
from blog import models
from blog.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordRequestForm
from blog.token import create_access_token


router = APIRouter(tags=["Login"])


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Incorrect username or password")
    verified_password = pwd_cxt.verify(request.password, user.hashed_password)
    if not verified_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username}
        )
    return {"access_token": access_token, "token_type": "bearer"}
    