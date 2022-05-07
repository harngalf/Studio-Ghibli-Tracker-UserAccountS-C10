#Python
from typing import Optional, List
from enum import Enum
from sqlalchemy.orm import Session


#Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl

#FastAPI 
from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form
from fastapi import APIRouter


# API Files
from src.database import Base, SessionLocal, engine
from schemas import user_movie_sch
from src import crud


usermovies = APIRouter()

# Dependency
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@usermovies.post(
    path="/user/{user_id}/movies/rate",
    #response_model=user_movie_sch.UserRating,
    status_code=status.HTTP_201_CREATED,
    summary="Rate a movie",
    tags=["User/Movies"],
    )
def rate_movie(
    #user_id: int,
    #movie_id: int,
    #user_ratinf: user_movie_sch.UserRatingBase,
    #db: Session = Depends(get_db)
):
    """
    ## Rate a movie

    This endpoint rate a movie with stars and emoji.

    ### Params:

        - Request body parameters as user_id, movie_id, rating_stars and rating_emoji.

    ### Returns:        
        - user_id: UUID -> The id of the user created 
        - movie_id: UUID -> The id of the movie created
        - rating_stars: Optional[int] -> The rating of the movie created
        - rating_emoji: Optional[str] -> The emoji rating of the movie created
    """
    #db_user_movies = crud.create_user_movies(db=db, user_id=user_id, movie_id=movie_id)
    #return db_user_movies
    pass

## Show a user movies
@usermovies.get(
    path="/users/{user_id}/movies",
    #response_model=List[UserRating],
    status_code=status.HTTP_200_OK,
    summary="Get user movies",
    tags=["User/Movies"]
)
def get_user_movies():
    """
    ## Get user movies

    This endpoint returns a list of movies rated by the user.

    ### Params:

        - user_id: UUID -> The id of the user created

    ### Returns:        
        - user_id: UUID -> The id of the user created 
        - movie_id: UUID -> The id of the movie rated
        - rating_stars: int -> The rating of the movie
        - rating_emoji: str -> The emoji rating of the movie
    """
    pass

