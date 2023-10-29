from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import models
from blog.database import get_db
from .. import schemas
from datetime import datetime

def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    all_blogs = []
    for blog in blogs:
        data = {"Author's first name":blog.author.first_name, "Author's last name":blog.author.last_name, "Title":blog.title, "Body":blog.body, "Created On":blog.created_on}
        all_blogs.append(data)
    return all_blogs


def create(blog:schemas.Blog, db: Session=Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    for each_blog in all_blogs:
        if blog.title == each_blog.title:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Blog with title already exists.")
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id = 1, created_on = datetime.now())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'Message': f"You've successfully created an article with title {blog.title}"}


def view_single_blog(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} does not exist.")
    return {"Author's first name":blog.author.first_name, "Author's last name":blog.author.last_name, "Title":blog.title, "Body":blog.body, "Created on":blog.created_on}


def blog_update(id, blog:schemas.UpdateBlog, db: Session = Depends(get_db)):
    if db.query(models.Blog).filter(models.Blog.id == id).first():
        db.query(models.Blog).filter(models.Blog.id == id).update({"title":blog.title, "body":blog.body})
        db.commit()
        return {"Message":f"You have successfully updated the blog with id {id}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} does not exist.")
    

def blog_delete(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first():
        blog.delete(synchronize_session=False)
        db.commit()
        return{"Message":"Blog successfully deleted!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id of {id} does not exist!")
    