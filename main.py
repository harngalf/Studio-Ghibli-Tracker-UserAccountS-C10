# #Python
from typing import Optional, List
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl

#FastAPI 
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form

# API Files
from schemas import movie_sch, user_sch, user_movie_sch
from models import movies_mod, user_mod, user_movies_mod
from src import crud
from src.database import SessionLocal, engine, Base
from routes import user_rt, user_movies_rt, movies_rt
from routes.user_rt import user
from routes.user_movies_rt import usermovies
from routes.movies_rt import movie

app = FastAPI()
app.include_router(user)
app.include_router(movie)
app.include_router(usermovies)


# # Dependency
# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
 
