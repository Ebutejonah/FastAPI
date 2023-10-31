from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import models
from blog.database import get_db


def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    all_blogs = []
    for blog in blogs:
        data = {"Author's first name":blog.author.first_name, "Author's last name":blog.author.last_name, "Title":blog.title, "Body":blog.body, "Created On":blog.created_on}
        all_blogs.append(data)
    return all_blogs


def view_single_blog(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} does not exist.")
    return {"Author's first name":blog.author.first_name, "Author's last name":blog.author.last_name, "Title":blog.title, "Body":blog.body, "Created on":blog.created_on}
