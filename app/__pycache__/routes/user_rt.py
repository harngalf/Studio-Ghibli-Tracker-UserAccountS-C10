#Python
from typing import Optional, List
from enum import Enum
#from cryptography.fernet import Fernet
#Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl

# SQLAlchemy
from sqlalchemy.orm import Session

#FastAPI 
from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form
from fastapi import APIRouter


# API Files
from src.database import Base, engine, SessionLocal
from schemas.user_sch import UserS, UserCreate, UserBase, UserLog, UserLogP
from src import crud

#key = Fernet.generate_key()
#f = Fernet(key)

user = APIRouter()

# Dependency
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@user.post(
    path="/user/singup", 
    response_model=UserS,
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    summary="Create a new user",
    )
async def create_user(
    user: UserCreate,
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
@user.post(
    path="/login",
    response_model=UserS,
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Login user",
    )
def login(
    user: UserLogP,
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
@user.get(
    path="/users",
    response_model=List[UserS],
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

## Show a user by id
@user.get(
    path="/users/{user_id}",
    response_model=UserS,
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
    