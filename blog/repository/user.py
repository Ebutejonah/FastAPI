from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from blog import models
from blog.database import get_db
from .. import schemas


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")
def register_user(user:schemas.User, db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Email provided already exists. Please Log In or provide another email for registration.")
    if not existing_user:
        if user.password == user.confirm_password:
            hashedPassword = pwd_cxt.hash(user.confirm_password)
            new_user = models.User(username=user.username, first_name = user.first_name, last_name = user.last_name, email = user.email, hashed_password = hashedPassword)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"Message": f"User with name {user.first_name} {user.last_name} successfully created."}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Passwords must match")
    

def user(username, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User not found")
    return {"Username":user.username, "First name":user.first_name, "Last name":user.last_name}