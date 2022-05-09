# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship

# API docs connection
import database


## User DB Model
class UserM(database.Base):
    __tablename__ = "users"
    
    user_id = Column(
        Integer,
        primary_key=True,
        index=True
    )    
    email = Column(
        String(255),
        unique=True,
        index=True
    )
    hashed_password = Column(
        String
    )
    user_name = Column(
        String(125),
        nullable=False
    )
    profile_pic = Column(
        String(255)
    )
    is_active = Column(
        Boolean, 
        default=True
    )

    user_movies = relationship(
        "UserMovie",
        back_populates="userM"
    )

## Movies DB Model
class MovieM(database.Base):
    __tablename__ = "movies"

    movie_id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    title = Column(
        String,
        nullable=False,
        index=True,
        unique=True
    )
    original_title = Column(
        String,
        nullable=True
    )
    original_title_romanized = Column(
        String,
        nullable=True
    )
    wiki_url = Column(
        String,
        nullable=True        
    )
    written_by = Column(
        String,
        nullable=True
    )
    director = Column(
       String,
       nullable=True
    )
    producer = Column(
        String,
        nullable=True
    )
    music_by = Column(
        String,
        nullable=True
    )
    release_date = Column(
        String,
        nullable=True
    )
    running_time = Column(
        String,
        nullable=True
    )
    rt_score = Column(
        Integer,
        nullable=True
    )
    movie_cover = Column(
        String,
        nullable=True
    )
    description = Column(
        Text,
        nullable=True
    )
    
    user_movies = relationship(
        "UserMovie",
        back_populates="movieU"
    )


## Movies/User DB Model
class UserMovie(database.Base):
    __tablename__ = "user_movies"

    user_movie_id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    watched = Column(
        Boolean,
        default=False
    )
    rating_stars = Column(
        Float,
        default=0
    )
    rating_emoji = Column(
        String(1),
        default="💚"
    )
    userM_id = Column(
        Integer,
        ForeignKey("user_id"),
        nullable=False
    )
    movieU_id = Column(
        Integer,
        ForeignKey("movie_id"),
        nullable=False
    )

    userM = relationship(
        "UserM",
        back_populates="user_movies"
    )
    movieU = relationship(
        "MovieM",
        back_populates="user_movies"
    )