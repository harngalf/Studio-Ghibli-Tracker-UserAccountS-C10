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
from src.database import Base
from schemas import movie_sch
from models import movies_mod
from src.database import SessionLocal, engine, Base
from src import crud

#movies_mod.Base.metadata.create_all(bind=engine)

movie = APIRouter()

# Dependency
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
 


@movie.post(
    path="/movies/create",
    response_model=movie_sch.MovieS, 
    status_code=status.HTTP_201_CREATED,
    tags=["Movies"],
    summary="Home page"
    )
def movie_create(
        movie: movie_sch.MovieCreate, 
        db: Session = Depends(crud.get_db)
    ):
    """
    ## Home

    This is the home endpoint path, returns the list of  all movies.

    ### Params:

        - movies: Movies

    ### Returns: 
        - title: sring
        - original_title: Optional[string]
        - original_title_romanized: Optional[string]
        - wiki_url: Optional[HttpUrl]
        - written_by: Optional[string]
        - description: Optional[string]
        - director: Optional[string]
        - producer: Optional[string]
        - music_by: Optional[string]
        - release_date: Optional[string]
        - running_time: Optional[str]
        - rt_score: Optional[str]
        - movie_cover: Optional[HttpUrl] 
    """
    db_movies = crud.get_movie_by_title(db, title=movie.title)
    if db_movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie is allready in the database"
        )
    return crud.create_movies(db=db, movie=movie)
  
    

# Show All Movies
@movie.get(
    path="/movies/",
    response_model=List[movie_sch.MovieS], 
    status_code=status.HTTP_200_OK,
    tags=["Movies"],
    summary="Home page"
    )
def movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Home

    This is the home endpoint path, returns the list of  all movies.

    ### Params:

        - skip: int
        - limit: int

    ### Returns: 
        - title: sring
        - original_title: Optional[string]
        - original_title_romanized: Optional[string]
        - wiki_url: Optional[HttpUrl]
        - written_by: Optional[string]
        - description: Optional[string]
        - director: Optional[string]
        - producer: Optional[string]
        - music_by: Optional[string]
        - release_date: Optional[string]
        - running_time: Optional[str]
        - rt_score: Optional[str]
        - movie_cover: Optional[HttpUrl] 
    """
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies
   
# Show Movie by title

@movie.get(
    path="/movies/{title}",
    response_model=movie_sch.MovieS,
    status_code=status.HTTP_200_OK,
    tags=["Movies"],
    summary="Home page"
    )
def movie_by_title(
        title: str,
        db: Session = Depends(get_db)
    ):
    """
    ## Movie by title

    This is the home endpoint path, returns a movies by title all information.
    
    ### Params:

    - title: string

    ### Returns:
        - title: sring
        - original_title: Optional[string]
        - original_title_romanized: Optional[string]
        - wiki_url: Optional[HttpUrl]
        - written_by: Optional[string]
        - description: Optional[string]
        - director: Optional[string]
        - producer: Optional[string]
        - music_by: Optional[string]
        - release_date: Optional[string]
        - running_time: Optional[str]
        - rt_score: Optional[str]
        - movie_cover: Optional[HttpUrl]
    """
    movie = crud.get_movie_by_title(db, title=title)
    return movie
