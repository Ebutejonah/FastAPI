from fastapi import FastAPI
from .routers import blog, user, login
from . import models
from .database import engine

app = FastAPI(title = "AltschoolAfrica Project(Backend Engineering). By Jonah Ebute", description = "An API built with FastAPI for a Blogging Platform")

models.Base.metadata.create_all(engine)

app.include_router(login.router)
app.include_router(blog.router)
app.include_router(user.router)
