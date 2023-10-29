from fastapi import APIRouter, Depends, status
from blog.database import get_db
from blog import schemas
from sqlalchemy.orm import Session
from ..repository import user
from blog.oauth2 import get_current_user

router = APIRouter(
    prefix = "/user",
    tags=['Users']
    )



@router.post("/", status_code = status.HTTP_201_CREATED)
def create_user(request:schemas.User, db : Session = Depends(get_db)):
    return user.register_user(request, db)


@router.get("/{username}", status_code=status.HTTP_200_OK)
def get_user(username, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return user.user(username,db)