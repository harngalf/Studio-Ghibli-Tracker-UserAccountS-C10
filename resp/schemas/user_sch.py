# Python
from typing import List, Optional

# PyDantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl


#FastAPI 
from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form
from fastapi.security import OAuth2PasswordBearer 

# API Files
from schemas.movie_sch import MovieS


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example="user@mailserver.com"
        )
    user_name: Optional[str] = Field(
        min_length=3,
        max_length=50,
        title="User nickname",
        description="User nickname",
        example="@John_Doe"
        )
    profile_pic: Optional[HttpUrl] = Field(
        None,
        example="https://my-user-pic.com"
        )


class UserLog(BaseModel):
    email: EmailStr = Field(
        ...,
        example="user@mailserver.com"
    )

class UserLogP(UserLog):
    hashed_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        title="Password",
        example = "password12345"
        )  

class UserCreate(UserBase):
    hashed_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        title="Password",
        example = "password12345"
        ) 



class UserS(UserBase):
    user_id: Optional[int] = Field(
        title="User ID",
        description="The unique ID of the user",
        exmaple="1"
    )
    is_active: bool   
    #movies = list[MovieS] = []       
    class Config:    
        orm_mode = True


