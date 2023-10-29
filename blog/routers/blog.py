from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from blog import schemas
from blog.oauth2 import get_current_user
from blog.database import get_db
from ..repository import blog


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
    )


@router.get("/")
def index(db : Session = Depends(get_db)):
    return blog.get_all(db)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_blog(request :schemas.Blog, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return blog.create(request, db)

@router.get("/{id}",status_code = status.HTTP_200_OK)
def view_blog(id, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return blog.view_single_blog(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:schemas.UpdateBlog, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return blog.blog_update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return blog.blog_delete(id, db)