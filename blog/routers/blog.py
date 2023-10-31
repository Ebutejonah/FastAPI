from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from blog import schemas
from blog.oauth2 import get_current_user
from blog.database import get_db
from ..repository import blog
from blog import models
from datetime import datetime


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
    )


@router.get("/")
def index(db : Session = Depends(get_db)):
    return blog.get_all(db)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_blog(blog:schemas.Blog, db: Session=Depends(get_db), current_user:models.User= Depends(get_current_user), get_current_user:schemas.User = Depends(get_current_user)):
    all_blogs = db.query(models.Blog).all()
    for each_blog in all_blogs:
        if blog.title == each_blog.title:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Blog with title already exists.")
    
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id = current_user.id, created_on = datetime.now())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'Message': f"You've successfully created an article with title {blog.title}"}

@router.get("/{id}",status_code = status.HTTP_200_OK)
def view_blog(id, db : Session = Depends(get_db), get_current_user:schemas.User = Depends(get_current_user)):
    return blog.view_single_blog(id, db)


@router.put("/{title}", status_code=status.HTTP_202_ACCEPTED)

#The update function works as expected. A blog can not be updated by a user that was not the author, but I keep geting the successful updated message

def update_blog(title, request:schemas.UpdateBlog, db : Session = Depends(get_db), current_user:models.User= Depends(get_current_user), get_current_user:schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.title == title, models.Blog.user_id == current_user.id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "You are not authorized to edit this blog.")
    blog.update({"title":request.title, "body":request.body})
    db.commit()
    return {"Message":f"You have successfully updated the blog"}
    

@router.delete("/{title}", status_code=status.HTTP_204_NO_CONTENT)

#The update function works as expected. A blog can not be deleted by a user that was not the author, but I keep geting the successful deleted message

def delete_blog(title, db: Session = Depends(get_db), current_user:models.User= Depends(get_current_user), get_current_user:schemas.User = Depends(get_current_user)):
    print(models.Blog.user_id)
    print(current_user.id)
    blog = db.query(models.Blog).filter(models.Blog.title == title, models.Blog.user_id == current_user.id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "You are not authorized to delete this blog.")
    
        
    blog.delete(synchronize_session=False)
    db.commit()
    return{"Message":"Blog successfully deleted!"}
    