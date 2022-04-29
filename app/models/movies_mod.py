
# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float, Date
from sqlalchemy.orm import relationship

# API docs connection
from src.database import Base


## Movies DB Model
class MovieM(Base):
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

    user_movies_mod = relationship("UserMovie", back_populates="movieU")

#Base.metadata.create_all(engine)