# #Python
from typing import Optional, List
from enum import Enum

# SQLAlchemy
from sqlalchemy.orm import Session
#FastAPI 
from fastapi import FastAPI
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form

# API Files
import crud, models, schemas
import database

Base = models.Base
engine = database.engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes

## User
@app.post(
    path="/user/singup", 
    response_model=schemas.UserS,
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    summary="Create a new user",
    )
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)    
    ):
    """
    ## Create new user

       -This endpoint creates a new user into the app and saves in the database.

    ### Request body parameters:

        - user: UserRegister -> The user to be created wirogth the required fields username, email and profile_pic

    ### Returns imto a json with contains the user created:
        -user_id: UUID -> The id of the user created
        -username: str -> The username of the user created
        -email: EmailStr -> The email of the user created
        -profile_pic: HTML -> The profile pic of the user created

    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user already exists")
    return crud.create_user(db=db, user=user)
    
# Login User
@app.post(
    path="/login",
    response_model=schemas.UserS,
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Login user",
    )
def login(
    user: schemas.UserLogP,
    db: Session = Depends(get_db)
):
    """
    # Login the user.

        This endpoint login the user and return the user logged.

    ## Params:
        - Request body parameters as usar name password and remember_me.

    ## Returns: 
        - the **username** logged.
    """
    db_userlogin = crud.get_user_by_email(db, email=user.email)
    if not db_userlogin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exists")
    if db_userlogin.hashed_password != user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
    return db_userlogin

## Show all users
@app.get(
    path="/users",
    response_model=list[schemas.UserS],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    tags=["User"],
    )
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get all users

    This endpoint returns all users.

    ### Params:
        - Request body parameters as user name password and remember_me.

    ### Returns: 
        - user_id: UUID -> The id of the user created
        - username: str -> The username of the user created
        - email: EmailStr -> The email of the user created
        - profile_pic: HTML -> The profile pic of the user created
    """
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

### Show a user by id
@app.get(
    path="/users/{user_id}",
    response_model=schemas.UserS,
    status_code=status.HTTP_200_OK,
    summary="Get user by id",
    tags=["User"]
    )
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    ## Get user by id

    This endpoint returns a user by id.

    ### Params:

        - user_id: UUID -> The id of the user created

    ### Returns:        
        - user_id: UUID -> The id of the user created 
        - username: str -> The username of the user created
        - email: EmailStr -> The email of the user created
        - profile_pic: HTML -> The profile pic of the user created
     
    """
    db_user_id = crud.get_user(db=db, user_id=user_id)
    if not db_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exists")
    return db_user_id
    
## Movies
@app.post(
    path="/movies/create",
    response_model=schemas.MovieS, 
    status_code=status.HTTP_201_CREATED,
    tags=["Movies"],
    summary="Home page"
    )
def movie_create(
        movie: schemas.MovieCreate, 
        db: Session = Depends(get_db)
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
  
    

### Show All Movies
@app.get(
    path="/movies/",
    response_model=list[schemas.MovieS], 
    status_code=status.HTTP_200_OK,
    tags=["Movies"],
    summary="Movies"
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
   
### Show Movie by title

@app.get(
    path="/movies/{title}",
    response_model=schemas.MovieS,
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

## User Movies
@app.post(
    path="/user/{user_id}/movies/",
    #response_model=schemas.UserRating,
    status_code=status.HTTP_201_CREATED,
    summary="Rate a movie",
    tags=["User/Movies"],
    )
def rate_movie(
    # userM_id: int,
    # movieU_id: int,
    # user_movies: schemas.UserMovieCreate,
    # db: Session = Depends(get_db)
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
    pass
    # return crud.create_user_movies(
    #     db=db, 
    #     user_movies=user_movies, 
    #     user_id=userM_id, 
    #     movie_id=movieU_id
    #     )

## Show a user movies
@app.get(
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

# Back Office API

@app.post(
    path="/backoffice/user/singup", 
    response_model=schemas.UserBOS,
    status_code=status.HTTP_201_CREATED,
    tags=["Backoffice User"],
    summary="Create a new backoffice user",
    )
async def create_user(
    user: schemas.UserBOCreate,
    db: Session = Depends(get_db)    
    ):
    """
    ## Create New Back Office User

       -This endpoint creates a new user into the Backoffice app and saves in the database.

    ### Request body parameters:

        - user: UserRegister -> The user to be created wirogth the required fields username, email and profile_pic

    ### Returns imto a json with contains the user created:
        -user_id: UUID -> The id of the user created
        -username: str -> The username of the user created
        -email: EmailStr -> The email of the user created
        -profile_pic: HTML -> The profile pic of the user created

    """
    db_user = crud.get_userBO_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user already exists")
    return crud.create_userBO(db=db, user=user)
    
# # Login BackOffice User
@app.post(
    path="/backoffice/user/login",
    response_model=schemas.UserBOS,
    status_code=status.HTTP_200_OK,
    tags=["Backoffice User"],
    summary="Login back office user",
    )
def login(
    user: schemas.UserBOLogP,
    db: Session = Depends(get_db)
):
    """
    # Login the back office user.

        This endpoint login the back office user and return the user logged.

    ## Params:
        - Request body parameters as usar name password and remember_me.

    ## Returns: 
        - the **username** logged.
    """
    db_userlogin = crud.get_userBO_by_email(db, email=user.email)
    if not db_userlogin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exists")
    if db_userlogin.hashed_password != user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
    return db_userlogin

# ## Show all backoffice users
@app.get(
    path="/backoffice/users",
    response_model=list[schemas.UserBOS],
    status_code=status.HTTP_200_OK,
    summary="Get all backoffice users",
    tags=["Backoffice User"],
    )
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get all backoffice users

    This endpoint returns all backoffice users.

    ### Params:
        - Request body parameters as user name password and remember_me.

    ### Returns: 
        - user_id: UUID -> The id of the user created
        - username: str -> The username of the user created
        - email: EmailStr -> The email of the user created
        - profile_pic: HTML -> The profile pic of the user created
    """
    users = crud.get_usersBO(db=db, skip=skip, limit=limit)
    return users

# ### Show a user by id
@app.get(
    path="/backoffice/users/{user_id}",
    response_model=schemas.UserBOS,
    status_code=status.HTTP_200_OK,
    summary="Get user by id",
    tags=["Backoffice User"]
    )
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    ## Get backoffice user by id

    This endpoint returns a backoffice user by id.

    ### Params:

        - user_id: UUID -> The id of the user created

    ### Returns:        
        - user_id: UUID -> The id of the user created 
        - username: str -> The username of the user created
        - email: EmailStr -> The email of the user created
        - profile_pic: HTML -> The profile pic of the user created
     
    """
    db_user_id = crud.get_userBO(db=db, user_id=user_id)
    if not db_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exists")
    return db_user_id

