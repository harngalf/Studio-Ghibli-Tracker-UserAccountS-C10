# Python
#from cryptography.fernet import Fernet

# SQLAlchemy
from sqlalchemy.orm import Session

# API files
from src.database import Base, engine, SessionLocal
#from schemas import movie_sch, user_sch, user_movie_sch
from schemas.user_sch import UserS, UserCreate, UserBase
from schemas.movie_sch import MovieS, MovieCreate, MovieBase
from schemas.user_movie_sch import UserMovieCreate, UserRating, UserRatingBase
#from models import movies_mod, user_mod, user_movies_mod
from models.movies_mod import MovieM
from models.user_mod import UserM
from models.user_movies_mod import UserMovie

#Base.metadata.create_all(engine)

# Dependency
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

def get_user(
    db: Session, 
    user_id: int
):
    return db.query(UserM).filter(UserM.user_id == user_id).first()

def get_user_by_email(
    db: Session, 
    email: str
):
    return db.query(UserM).filter(UserM.email == email).first()

def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
):
    return db.query(UserM).offset(skip).limit(limit).all()

def create_user(
    db: Session, 
    user: UserS
):
    fake_hashed_password = user.hashed_password + "not really hashed"
    db_user = UserM(
        # **user.dict()
        email=user.email,
        hashed_password=fake_hashed_password,
        user_name=user.user_name,        
        profile_pic=user.profile_pic
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_movies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
):
    return db.query(MovieM).offset(skip).limit(limit).all()


def get_movie(
    db: Session, 
    movie_id: int,
    title: str
):
    return db.query(MovieM).filter(MovieM.movie_id == movie_id).first()  

def get_movie_by_title(
    db: Session, 
    title: str
):
    return db.query(MovieM).filter(MovieM.title == title).first()

def create_movies(
    db: Session,
    movie: MovieS
):
    db_movies = MovieM(**movie.dict())
    db.add(db_movies)
    db.commit()
    db.refresh(db_movies)
    return db_movies


def create_user_movies(
    db: Session, 
    user_movies: UserRating
):
    # db_user_movies = UserMovie(
    #     user_id=user_movies.user_id,
    #     movie_id=user_movies.movie_id,
    #     rating_stars=user_movies.rating_stars,
    #     rating_emoji=user_movies.rating_emoji
    # )
    db_user_movies = UserMovie(**user_movies.dict())
    db.add(db_user_movies)
    db.commit()
    db.refresh(db_user_movies)
    return db_user_movies
