# Python
from typing import List, Optional

# PyDantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl


# Schemas

## User Movies
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
    pass

class UserRating(UserRatingBase):
    user_rating_id: Optional[int]
    movieU_id: Optional[int] = Field(
        title="Movie ID",
        description="The unique ID of the movie",
        example=1
    )
    userM_id: Optional[int] = Field(
        title="User ID",
        description="The unique ID of the user",
        example=1
    )


    class Config:
        orm_mode = True

## User
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
    movieU: UserRating = []       
    class Config:    
        orm_mode = True

class MovieBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        title="Movie title",
        description="Movie title information",
        example="Castle in the Sky"
    )
    description: Optional[str] = Field(
        default=None,
        title="Movie description",
        description="Movie description information resume",
        example="The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world."
    )


## Movies
class MovieCreate(MovieBase):
    original_title: Optional[str] = Field(
        default=None,
        max_length=255,
        title="Original Movie title",
        description="Original Movie title information",
        example="天空の城ラピュタ"
    )
    original_title_romanized: Optional[str] = Field(
        default=None,
        max_length=255,
        title="Original Movie title in romanized fomrm",
        description="Original Movie title information in romanized form information",
        example="Tenkū no shiro Rapyuta"
    )
    wiki_url: Optional[HttpUrl] = Field(
        default=None,
        title="Wikipedia URL",
        description="Wikipedia URL information link",
        example="https://ghibli.fandom.com/wiki/Castle_in_the_Sky"
    )
    written_by: Optional[str] = Field(
        default=None,
        max_length=255,
        title="Written by",
        description="Written by information",
        example="Hayao Miyazaki"
    )
    director: Optional[str] = Field(
        default=None,
        title="Director of the movie",
        description="Director of the movie information",
        example="Hayao Miyazaki"
    )
    producer: Optional[str] = Field(
        default=None,
        title="Producer of the movie",
        description="Producer of the movie information",
        example="Isao Takahata"
    )
    music_by: Optional[str] = Field(
        default=None,
        title="Music by",
        description="Music by information",
        example="Joe Hisaishi"
    )
    release_date: Optional[str] = Field(
        default=None,
        title="Release date of the movie",
        description="Release date year of the movie information",
        example="1988"
    )
    running_time: Optional[str] = Field(
        default=None,
        title="Running time of the movie in minutes",
        description="Running time of the movie in minutes information",
        example="89"
    )
    rt_score: Optional[str] = Field(
        default=None,
        title="Movie rating from Rotten Tomatoes",
        description="Movie rating from Rotten Tomatoes information",
        example="97"
    )
    movie_cover: Optional[HttpUrl] = Field(
        default=None,
        title="Movie cover URL",
        description="Movie cover URL information",
        example="https://image.tmdb.org/t/p/w600_and_h900_bestv2/npOnzAbLh6VOIu3naU5QaEcTepo.jpg"
    )

class MovieS(MovieCreate):
    movie_id: Optional[str]
    class Config:
        orm_mode = True

# Back Office

## Users
class UserBOBase(BaseModel):
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


class UserBOLog(BaseModel):
    email: EmailStr = Field(
        ...,
        example="user@mailserver.com"
    )

class UserBOLogP(UserLog):
    hashed_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        title="Password",
        example = "password12345"
        )  

class UserBOCreate(UserBase):
    hashed_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        title="Password",
        example = "password12345"
        ) 



class UserBOS(UserBase):
    user_id: Optional[int] = Field(
        title="User ID",
        description="The unique ID of the user",
        exmaple="1"
    )
    is_active: bool        
    class Config:    
        orm_mode = True

