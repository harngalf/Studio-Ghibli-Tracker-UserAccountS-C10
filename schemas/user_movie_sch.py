# Python
from typing import List, Optional

# PyDantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl

# API Files
from schemas.user_sch import UserS
from schemas.movie_sch import MovieS

class UserRatingBase(BaseModel):
    rating_stars: Optional[int] = Field(
        default=None,
        title="Rating of the movie",
        description="Rating of the movie user quality",
        example=5
    )
    rating_emoji: Optional[str] = Field(
        default=None,
        title="Emoji rating of the movie",
        description="Emoji rating of the movie user quality",
        example="💚"
    )

class UserMovieCreate(UserRatingBase):
    movie_id: int = Field(
        ...,
        title="Movie ID",
        description="The unique ID of the movie",
        example=1
    )
    user_id: int = Field(
        ...,
        title="User ID",
        description="The unique ID of the user",
        example=1
    )

class UserRating(UserRatingBase):
    user_rating_id: int = Field(
        ...
    )
    #userM_id: int
    #movieU_id: int
    user: UserS
    movies: list[MovieS] = []
    class Config:
        orm_mode = True