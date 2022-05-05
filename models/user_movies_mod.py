
# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float, Date
from sqlalchemy.orm import relationship

# API docs connection
from src.database import Base, engine


## Movies/User DB Model
class UserMovie(Base):
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

    #userM = relationship("UserM", back_populates="user_movies_u")
    #movieU = relationship("MovieM", back_populates="user_movies_m")

Base.metadata.create_all(engine)